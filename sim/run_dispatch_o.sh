#!/bin/bash
# O 车道（ornith-1.5-35b @ Mac Studio）单独恢复启动器（规约 L-6/R-1）。
# 场景：LM Studio 模型被卸载后管理员已 `lms load ornith-1.5-35b` 恢复，
# 本脚本仅重启 O1–O3 子车道，不影响其他在跑车道的进程与旗标。
# 用法: bash sim/run_dispatch_o.sh [tasks_dir]
set -u
cd "$(dirname "$0")"
TASKS_DIR="${1:-dispatch_tasks}"
PIDS=()
for L in O1 O2 O3; do
  setsid nohup bash lane_runner.sh "$L" "http://<内网地址已脱敏>:1234/v1" "ornith-1.5-35b" \
      "$TASKS_DIR/tasks_${L}.txt" 2400 4800 </dev/null >/dev/null 2>&1 &
  PIDS+=($!)
  echo "子车道 $L 启动 (PID $!): ornith-1.5-35b @ MacStudio (tokens 2400/4800)"
done
wait "${PIDS[@]}"
echo "O 车道全部结束。旗标目录: pilot/results/dispatch_flags/"
