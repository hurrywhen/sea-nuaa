#!/bin/bash
# 三节点 + OpenRouter 云并行调度（规约 R-5/S8）：P1–P12 主验证 LLM 队列层
# 车道 = (端点, 模型家族)，满足主体/评分器/红队 ≥3 家族分离原则：
#   O1/O2/O3: Mac Studio <内网地址已脱敏> LM Studio :1234  ornith-1.5-35b   (主力, 3 分片)
#   C1..C6:   OpenRouter 付费  ling-3.0-flash                            (主力, 6 分片, ~$3)
#   Q:        已退役（规约 R-11：qwen 全量上云至 QC；node-a 转产 gemma）
#   G1/G2:    node-d    <内网地址已脱敏>  Ollama   :11434  gemma4:26b        (锚点 run 1–5)
#   GA1/GA2:  node-a    <内网地址已脱敏>  Ollama   :11434  gemma4:26b        (锚点 run 6–10)
#   F:        已裁撤（规约 R-18：配额硬顶+付费容量瓶颈；产物归档 archive_family_F/）
#   QC:       OpenRouter 付费  qwen/qwen3.8-27b                          (锚点 run 2–10 + 电池)
# 密钥（规约 R-6）：OPENROUTER_API_KEY 不入库，经 gitignored 的 sim/.openrouter_key 注入。
# 注意（运维教训）：Mac 上 LM Studio 运行期间禁用同机 Ollama 大模型换入换出；
# node-a 上 qwen3.8-27b 常驻 VRAM（34.5GB），不要再加载 ornith/flash。
#
# 用法: bash sim/run_dispatch_3node.sh <tasks_dir> [只启动这些车道，空格分隔]
set -u
cd "$(dirname "$0")"
chmod +x lane_runner.sh
TASKS_DIR="${1:-dispatch_tasks}"
ONLY="${2:-}"   # 可选：仅启动列出的车道（如 "QC G1 G2 GA1 GA2"），空 = 全部

# 规约 R-6：云密钥注入（缺失则云车道预检失败、本地车道不受影响）
[ -f .openrouter_key ] && source .openrouter_key
ORK="${OPENROUTER_API_KEY:-}"

PIDS=()
launch() {
  # $1 lane  $2 base_url  $3 model  $4 init_tokens  $5 cap_tokens  $6 api_key(可空)
  # $7 min_interval（可选，规约 R-7 免费配额节拍，秒）
  # $8 cost_cap（可选，规约 R-8/R-10 成本熔断额，美元/进程）
  # $9 num_ctx（可选，规约 R-11 node-a 防 OOM 上下文限制）
  # $10 provider_order（可选，规约 R-14 OpenRouter 提供商路由，逗号分隔）
  # setsid 完全脱离会话：防止调用方 shell 退出时进程组被连带终止（运维教训 2026-10-05）
  local lane="$1"
  if [ -n "$ONLY" ] && ! echo " $ONLY " | grep -q " $lane "; then
    return 0   # 车道过滤：未列入则跳过（R-1 部分恢复）
  fi
  # 幂等守卫（运维教训 2026-10-08：重复启动会双写同一 jsonl；
  # 锚定 ^ 防止包装壳的 cmdline 文本误匹配）
  if pgrep -f "^bash lane_runner.sh $lane " >/dev/null 2>&1; then
    echo "[skip] $lane 已在运行，跳过（避免双写）"
    return 0
  fi
  local envp=()
  [ -n "${7:-}" ] && envp+=("SEA_MIN_INTERVAL=$7")
  [ -n "${8:-}" ] && envp+=("SEA_COST_CAP=$8")
  [ -n "${9:-}" ] && envp+=("SEA_NUM_CTX=$9")
  [ -n "${10:-}" ] && envp+=("SEA_PROVIDER_ORDER=${10}")
  env ${envp[@]+"${envp[@]}"} setsid nohup bash lane_runner.sh "$lane" "$2" "$3" \
      "$TASKS_DIR/tasks_${lane}.txt" "$4" "$5" "${6:-}" </dev/null >/dev/null 2>&1 &
  PIDS+=($!)
  echo "子车道 $lane 启动 (PID $!): $3 @ $2 (tokens $4/$5${7:+, 节拍 ${7}s}${8:+, 熔断 \$${8}})"
}
launch O1 "http://<内网地址已脱敏>:1234/v1" "ornith-1.5-35b" 2400 4800
launch O2 "http://<内网地址已脱敏>:1234/v1" "ornith-1.5-35b" 2400 4800
launch O3 "http://<内网地址已脱敏>:1234/v1" "ornith-1.5-35b" 2400 4800
launch G1 "http://<内网地址已脱敏>:11434/v1" "gemma4:26b" 1200 2400
launch G2 "http://<内网地址已脱敏>:11434/v1" "gemma4:26b" 1200 2400
launch GA1 "http://<内网地址已脱敏>:11434/v1" "gemma4c4k" 1200 2400
launch GA2 "http://<内网地址已脱敏>:11434/v1" "gemma4c4k" 1200 2400
# O 家族增援（规约 R-16）：node-a/node-d 转产 ornith（G 完成后启用；O 档 2400/4800）
launch OA1 "http://<内网地址已脱敏>:11434/v1" "ornith-c8k" 2400 4800
launch OA2 "http://<内网地址已脱敏>:11434/v1" "ornith-c8k" 2400 4800
launch OD1 "http://<内网地址已脱敏>:11434/v1" "ornith-1.5:35b" 2400 4800
launch OD2 "http://<内网地址已脱敏>:11434/v1" "ornith-1.5:35b" 2400 4800
# 云车道（规约 S8）：C 付费主力 6 分片（成本熔断 $2/进程，规约 R-8 内置于后端）；
# F 免费锚点单流 + 100s 配额节拍（≤864 次/日，规约 R-7）
launch C1 "https://openrouter.ai/api/v1" "inclusionai/ling-3.0-flash" 1200 2400 "$ORK"
launch C2 "https://openrouter.ai/api/v1" "inclusionai/ling-3.0-flash" 1200 2400 "$ORK"
launch C3 "https://openrouter.ai/api/v1" "inclusionai/ling-3.0-flash" 1200 2400 "$ORK"
launch C4 "https://openrouter.ai/api/v1" "inclusionai/ling-3.0-flash" 1200 2400 "$ORK"
launch C5 "https://openrouter.ai/api/v1" "inclusionai/ling-3.0-flash" 1200 2400 "$ORK"
launch C6 "https://openrouter.ai/api/v1" "inclusionai/ling-3.0-flash" 1200 2400 "$ORK"
# F 家族已裁撤（规约 R-18，2026-10-12）
# QC 云端增援（规约 R-10）：同型号付费 qwen3.8-27b 分担 Q 的 run 6–10，熔断 $5/进程
launch QC "https://openrouter.ai/api/v1" "qwen/qwen3.8-27b" 1200 2400 "$ORK" "" 5

echo "监控: python3 -m sea_pilot.dispatch_progress --watch 60"
wait "${PIDS[@]}"
echo "全部车道结束。旗标目录: pilot/results/dispatch_flags/"
