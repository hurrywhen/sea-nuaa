#!/bin/bash
# 串行驱动：任务1 ornith 扩样重放 → 任务2 gemma4 跨家族重放 → 任务3 H8 v2 双模型
# 严格串行（单推理服务，避免并发阻塞）；每步失败不中断链条；全部完成落 sequence_done.flag
cd "$(dirname "$0")"
mkdir -p pilot/results
rm -f pilot/results/sequence_done.flag

ts() { date "+%F %T"; }

echo "[$(ts)] === SEQUENCE START ==="

echo "[$(ts)] Task1: ornith-1.5-35b × P3 重放 30d×8agents（断点续跑：tag=ornith30）"
SEA_LLM_BASE_URL=http://<内网地址已脱敏>:1234/v1 SEA_LLM_API_KEY=lm-studio \
SEA_LLM_MODEL=ornith-1.5-35b \
  python3 -m sea_pilot.run_llm_replay --days 30 --agents 8 --tag ornith30 \
  || echo "[$(ts)] Task1 FAILED（可重跑续传）"

echo "[$(ts)] Task2: gemma4:31b-it-bf16 × P3 重放 30d×8agents（tag=gemma30）"
SEA_LLM_BASE_URL=http://<内网地址已脱敏>:11434/v1 SEA_LLM_API_KEY=ollama \
SEA_LLM_MODEL=gemma4:31b-it-bf16 \
  python3 -m sea_pilot.run_llm_replay --days 30 --agents 8 --tag gemma30 \
  || echo "[$(ts)] Task2 FAILED（可重跑续传）"

echo "[$(ts)] Task3a: H8 v2 @ ornith"
SEA_LLM_BASE_URL=http://<内网地址已脱敏>:1234/v1 SEA_LLM_API_KEY=lm-studio \
SEA_LLM_MODEL=ornith-1.5-35b \
  python3 -m sea_pilot.h8_battery_v2 --model-tag ornith --n-a 20 --n-b 10 --n-c 20 \
  || echo "[$(ts)] Task3a FAILED（可重跑续传）"

echo "[$(ts)] Task3b: H8 v2 @ gemma4"
SEA_LLM_BASE_URL=http://<内网地址已脱敏>:11434/v1 SEA_LLM_API_KEY=ollama \
SEA_LLM_MODEL=gemma4:31b-it-bf16 \
  python3 -m sea_pilot.h8_battery_v2 --model-tag gemma4 --n-a 20 --n-b 10 --n-c 20 \
  || echo "[$(ts)] Task3b FAILED（可重跑续传）"

echo "[$(ts)] === SEQUENCE DONE ==="
touch pilot/results/sequence_done.flag
