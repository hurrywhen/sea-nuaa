#!/bin/bash
# 流 B：node-a llama.cpp :11435（qwen3.8-27b GGUF）——重放扩样 → H8 v2
# 与流 A 并行（不同推理进程；若 node-a 资源吃紧则两流各自变慢，不互相失败）
cd "$(dirname "$0")"
ts() { date "+%F %T"; }
export SEA_LLM_BASE_URL=http://<内网地址已脱敏>:11435/v1
export SEA_LLM_API_KEY=llamacpp
export SEA_LLM_MODEL=~/models/qwen3.8-27b/Qwen3.8-27B-UD-Q4_K_XL.gguf

echo "[$(ts)] === STREAM B START (qwen3.8-27b @ node-a:11435) ==="

echo "[$(ts)] B1: 重放 30d×8agents (tag=qwen38na)"
python3 -m sea_pilot.run_llm_replay --days 30 --agents 8 --tag qwen38na \
  || echo "[$(ts)] B1 FAILED（可重跑续传）"

echo "[$(ts)] B2: H8 v2 (tag=qwen38na)"
python3 -m sea_pilot.h8_battery_v2 --model-tag qwen38na --n-a 20 --n-b 10 --n-c 20 \
  || echo "[$(ts)] B2 FAILED（可重跑续传）"

echo "[$(ts)] === STREAM B DONE ==="
touch pilot/results/stream_b_done.flag
