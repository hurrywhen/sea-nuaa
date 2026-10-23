#!/bin/bash
# 三节点车道执行器：单个车道（= 一个模型家族端点）串行执行任务清单。
# 用法: lane_runner.sh <lane_name> <base_url> <model> <task_file>
# 任务清单格式（每行一条，# 开头为注释）：
#   <模块> <参数...>        例如: sea_pilot.run_llm_replay --days 90 --agents 30 --tag o_r01
# 设计原则（来自运维教训 2026-09-27/28）：
#   1. 每车道串行（单实例推理，避免同机内存挤压）；
#   2. 每条任务原子落盘 + 断点续跑（模块内已有参与者级 tmp+rename）；
#   3. 模型一致性守卫：预检校验响应 model 字段与车道声明一致；
#   4. 内容有效性健康探测（非仅 HTTP 200）：预检要求输出非空且非退化重复。
set -u
cd "$(dirname "$0")"   # 固定工作目录为 sim/（pilot/results 相对路径与 python -m 包路径依赖它）
LANE="$1"; BASE_URL="$2"; MODEL="$3"; TASKS="$4"
INIT_TOK="${5:-1200}"; CAP_TOK="${6:-2400}"   # 规约 P-4：按家族分档的思考预算
API_KEY="${7:-${SEA_LLM_API_KEY:-ollama}}"    # 规约 R-6：密钥经参数/环境注入，不入库
ts() { date "+%F %T"; }
LOG="pilot/results/dispatch_${LANE}.log"
FLAGDIR="pilot/results/dispatch_flags"
mkdir -p "$FLAGDIR"

export SEA_LLM_BASE_URL="$BASE_URL"
export SEA_LLM_API_KEY="$API_KEY"
export SEA_LLM_MODEL="$MODEL"
export SEA_MAX_TOKENS_INIT="$INIT_TOK"
export SEA_MAX_TOKENS_CAP="$CAP_TOK"
export SEA_REQUIRE_REAL_BACKEND=1   # 调度模式：禁用 Mock 回退（规约 WU-4 强化）

# ---- 预检：健康探测 + 模型一致性守卫（实现于 sea_pilot.preflight，规约 V-1/V-6）----
echo "[$(ts)] [$LANE] preflight $MODEL @ $BASE_URL" | tee -a "$LOG"
if ! python3 -m sea_pilot.preflight "$BASE_URL" "$MODEL" "$API_KEY" >> "$LOG" 2>&1; then
  echo "[$(ts)] [$LANE] PREFLIGHT FAILED，车道退出" | tee -a "$LOG"; exit 1
fi
echo "[$(ts)] [$LANE] preflight OK" | tee -a "$LOG"

# ---- 串行执行任务清单 ----
FAILED_COUNT=0
while IFS= read -r line; do
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  # 任务完成标记：以整行命令的哈希为旗标，支持中断后精确续跑
  key=$(echo -n "$line" | md5sum | cut -c1-12)
  if [ -f "$FLAGDIR/${LANE}_${key}.done" ]; then
    echo "[$(ts)] [$LANE] SKIP(已完成): $line" >> "$LOG"; continue
  fi
  echo "[$(ts)] [$LANE] RUN: $line" | tee -a "$LOG"
  if python3 -m $line >> "$LOG" 2>&1; then
    touch "$FLAGDIR/${LANE}_${key}.done"
    echo "[$(ts)] [$LANE] DONE: $line" >> "$LOG"
  else
    echo "[$(ts)] [$LANE] FAILED（保留现场，可重跑续传）: $line" | tee -a "$LOG"
    FAILED_COUNT=$((FAILED_COUNT + 1))
  fi
done < "$TASKS"
# 规约 WU-4：有失败任务时不盖总完成旗标（防止进度条假 ✅）
if [ "$FAILED_COUNT" -eq 0 ]; then
  echo "[$(ts)] [$LANE] ALL TASKS FINISHED" | tee -a "$LOG"
  touch "$FLAGDIR/${LANE}_ALL.done"
else
  echo "[$(ts)] [$LANE] 队列结束但有 $FAILED_COUNT 条 FAILED（未盖总旗标，重跑续补）" | tee -a "$LOG"
fi
