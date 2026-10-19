"""Provider-neutral completion call for CrossSource (Anthropic + OpenAI), with usage accounting.

    text = complete(model, system, user, max_tokens, schema=None)

`model` is a bare id. Ids starting with "gpt-", "o1", "o3", "o4" or prefixed
"openai:" go to OpenAI; everything else goes to Anthropic. `schema` is the
harness's {"type": "json_schema", "schema": {...}} dict; with it, the reply is
constrained JSON (Anthropic output_config.format / OpenAI response_format).

Every call's token usage is appended to USAGE, and cost() prices it from
PRICES ($ per million tokens; override with CROSSSOURCE_PRICES='{"model": [in, out]}').
"""

import json
import os
import threading

PRICES = {
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-opus-4-8": (5.00, 25.00),
}
PRICES.update({k: tuple(v) for k, v in json.loads(os.environ.get("CROSSSOURCE_PRICES", "{}")).items()})

USAGE = []
_lock = threading.Lock()
_clients = {}


def is_openai(model: str) -> bool:
    return model.startswith(("openai:", "gpt-", "o1", "o3", "o4"))


def _client(provider):
    if provider not in _clients:
        if provider == "openai":
            import openai
            _clients[provider] = openai.OpenAI()
        else:
            import anthropic
            _clients[provider] = anthropic.Anthropic()
    return _clients[provider]


def _record(model, role, tin, tout):
    with _lock:
        USAGE.append({"model": model, "role": role, "input_tokens": tin, "output_tokens": tout})


def complete(model: str, system: str, user: str, max_tokens: int = 1500, schema: dict | None = None, role: str = "") -> str:
    if is_openai(model):
        name = model.removeprefix("openai:")
        kwargs = {}
        if schema:
            kwargs["response_format"] = {"type": "json_schema",
                                         "json_schema": {"name": "verdict", "strict": True, "schema": schema["schema"]}}
        r = _client("openai").chat.completions.create(
            model=name, max_completion_tokens=max_tokens,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}], **kwargs)
        _record(name, role, r.usage.prompt_tokens, r.usage.completion_tokens)
        return r.choices[0].message.content or ""
    kwargs = {"output_config": {"format": schema}} if schema else {}
    # current Claude models think adaptively and thinking counts toward max_tokens
    r = _client("anthropic").messages.create(
        model=model, max_tokens=max(max_tokens, 8000), system=system,
        messages=[{"role": "user", "content": user}], **kwargs)
    _record(model, role, r.usage.input_tokens, r.usage.output_tokens)
    if r.stop_reason == "refusal":
        raise RuntimeError(f"{model} refused")
    return next((b.text for b in r.content if b.type == "text"), "")


def cost(usage=None):
    """Per-model token totals and $ cost (None where the model has no price)."""
    out = {}
    for u in usage if usage is not None else USAGE:
        m = out.setdefault(u["model"], {"calls": 0, "input_tokens": 0, "output_tokens": 0})
        m["calls"] += 1
        m["input_tokens"] += u["input_tokens"]
        m["output_tokens"] += u["output_tokens"]
    for name, m in out.items():
        p = PRICES.get(name)
        m["usd"] = round((m["input_tokens"] * p[0] + m["output_tokens"] * p[1]) / 1e6, 4) if p else None
    return out
