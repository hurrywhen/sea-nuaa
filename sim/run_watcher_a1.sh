#!/bin/bash
# 看守：等流 A 的 H8 v2 完成（stream_a_done.flag）后，用修复版 ID 解析器续跑 A1 重放
cd "$(dirname "$0")"
ts() { date "+%F %T"; }
echo "[$(ts)] watcher: 等待 stream_a_done.flag（A2 H8 v2 @ gemma 进行中）…"
while [ ! -f pilot/results/stream_a_done.flag ]; do sleep 60; done
echo "[$(ts)] watcher: A2 完成，续跑 A1 重放（gemma4:26b, tag=gemma26na, 断点续传+空记录清理）"
SEA_LLM_BASE_URL=http://<内网地址已脱敏>:11434/v1 SEA_LLM_API_KEY=ollama SEA_LLM_MODEL=gemma4:26b \
  python3 -m sea_pilot.run_llm_replay --days 30 --agents 8 --tag gemma26na \
  || echo "[$(ts)] watcher: A1 续跑失败（可再次重跑，断点续传）"
echo "[$(ts)] watcher: A1 完成"
touch pilot/results/stream_a2_done.flag
