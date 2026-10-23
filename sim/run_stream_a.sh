#!/bin/bash
# 流 A：node-a Ollama :11434（gemma4:26b）——重放扩样 → H8 v2
cd "$(dirname "$0")"
ts() { date "+%F %T"; }
export SEA_LLM_BASE_URL=http://<内网地址已脱敏>:11434/v1
export SEA_LLM_API_KEY=ollama
export SEA_LLM_MODEL=gemma4:26b

echo "[$(ts)] === STREAM A START (gemma4:26b @ node-a:11434) ==="

echo "[$(ts)] A1: 重放 30d×8agents (tag=gemma26na)"
python3 -m sea_pilot.run_llm_replay --days 30 --agents 8 --tag gemma26na \
  || echo "[$(ts)] A1 FAILED（可重跑续传）"

echo "[$(ts)] A2: H8 v2 (tag=gemma26na)"
python3 -m sea_pilot.h8_battery_v2 --model-tag gemma26na --n-a 20 --n-b 10 --n-c 20 \
  || echo "[$(ts)] A2 FAILED（可重跑续传）"

echo "[$(ts)] === STREAM A DONE ==="
touch pilot/results/stream_a_done.flag
