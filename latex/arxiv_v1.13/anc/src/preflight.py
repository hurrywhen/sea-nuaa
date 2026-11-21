"""车道预检守卫（调度规约 V-1）：内容有效性 + 模型一致性。

用法：python3 -m sea_pilot.preflight <base_url> <model>
退出码 0 = 通过；1 = 拒绝（原因打印到 stderr）。
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request


def validate_response(d: dict) -> str:
    """校验一次 chat/completions 响应，返回服务端 model 字段。

    兼容三种推理字段形态：content（直接回答）、reasoning_content（ornith/qwen）、
    reasoning（gemma/Ollama）。空内容与退化重复（如 '////...'）一律拒绝。
    """
    c = d["choices"][0]["message"]
    content = (c.get("content") or "") + (c.get("reasoning_content") or "") + (c.get("reasoning") or "")
    assert content.strip(), "empty content"
    assert content.count("/") <= 20, "degenerate repetition"
    return str(d.get("model") or "")


def preflight(base_url: str, model: str, timeout: int = 120,
              api_key: str | None = None) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "回复两个字：正常"}],
        "max_tokens": 512,
    }).encode()
    headers = {"Content-Type": "application/json"}
    key = api_key if api_key is not None else os.environ.get("SEA_LLM_API_KEY", "")
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions", data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read())
    got = validate_response(d)
    assert not got or got == model, f"model mismatch: {got} != {model}"
    return got


def main() -> None:
    base_url, model = sys.argv[1], sys.argv[2]
    api_key = sys.argv[3] if len(sys.argv) > 3 else None
    try:
        got = preflight(base_url, model, api_key=api_key)
        print(f"preflight OK: model={got}")
    except Exception as e:  # noqa: BLE001
        print(f"PREFLIGHT_FAIL: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
