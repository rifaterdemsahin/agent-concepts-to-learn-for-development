"""Grocery-bot harness: one file, six concepts, no API key needed.
Run:  python poc/bot.py
Each section is tagged [REQ] [ARCH] [LLM] [OUT] [MCP] [LIFE] and feeds the next."""
import json, re

# ---- [REQ] Understanding requirements -> an executable spec -------------
SPEC = {"goal": "restock low items", "min_basket_gbp": 50, "max_lines": 12,
        "low_stock_below": 2, "done_when": "order_placed"}   # spec drives validator + prompt

# ---- [MCP] Tools exposed by a server, called via JSON-RPC-shaped messages
PANTRY = {"milk": 0, "eggs": 2, "rice": 1, "yoghurt": 0}
PRICE = {"milk": 1.5, "eggs": 2.8, "rice": 3.2, "yoghurt": 2.0}
TOOLS = {
 "list_pantry": {"description": "Current stock per item", "inputSchema": {"type": "object"},
                 "fn": lambda a: PANTRY},
 "place_order": {"description": "Order {item: qty}", "inputSchema": {"type": "object"},
                 "fn": lambda a: {"status": "order_placed", "total": basket_total(a["basket"])}},
}
def mcp_handle(req):                       # what an MCP server does: tools/list + tools/call
    if req["method"] == "tools/list":
        return {"tools": [{"name": n, **{k: v for k, v in t.items() if k != "fn"}} for n, t in TOOLS.items()]}
    t = TOOLS[req["params"]["name"]]
    return {"content": t["fn"](req["params"]["arguments"])}

def basket_total(b): return round(sum(PRICE[i] * q for i, q in b.items()), 2)

# ---- [LLM] Fundamentals: stateless text-in/text-out, finite context ------
def tokens(msgs): return sum(len(m["content"]) for m in msgs) // 4   # ~4 chars/token
def mock_llm(msgs, temperature=0):
    """Stand-in for a real model. Sees the whole history every call (no memory)."""
    assert tokens(msgs) < 8000, "context window exceeded"
    last = msgs[-1]
    if last["role"] == "user":
        return '{"action":"tool","name":"list_pantry","arguments":{}}'
    if last["role"] == "tool" and "milk" in last["content"]:
        bad = {"milk": 2, "yoghurt": 2, "rice": 1}                  # first try ignores min basket
        return "Sure!\n```json\n" + json.dumps({"action": "order", "basket": bad}) + "\n```"
    if last["role"] == "error":
        good = {"milk": 6, "yoghurt": 6, "rice": 4, "eggs": 6}
        return json.dumps({"action": "order", "basket": good})
    return json.dumps({"action": "done", "summary": last["content"]})

# ---- [OUT] Output handling: extract -> parse -> validate -> feed errors back
def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m: raise ValueError("no JSON found")
    return json.loads(m.group(0))
def validate(out):
    if out["action"] == "order":
        b = out["basket"]
        if not set(b) <= set(PRICE): return "unknown item"
        if len(b) > SPEC["max_lines"]: return "too many lines"
        if basket_total(b) < SPEC["min_basket_gbp"]:
            return f"basket £{basket_total(b)} is below minimum £{SPEC['min_basket_gbp']}"
    return None

# ---- [ARCH] Agent architecture: the harness loop around the model -------
def run(max_steps=8):
    msgs = [{"role": "user", "content": json.dumps(SPEC)}]           # spec becomes the prompt
    for step in range(max_steps):                                    # bounded loop = safety
        raw = mock_llm(msgs)
        try: out = parse(raw)
        except ValueError as e:
            msgs.append({"role": "error", "content": str(e)}); continue
        err = validate(out)
        if err:
            print(f"[{step}] REJECTED: {err}"); msgs.append({"role": "error", "content": err}); continue
        if out["action"] == "tool":
            res = mcp_handle({"method": "tools/call", "params": {"name": out["name"], "arguments": out["arguments"]}})
            print(f"[{step}] tool {out['name']} -> {res['content']}")
            msgs.append({"role": "tool", "content": json.dumps(res["content"])})
        elif out["action"] == "order":
            res = mcp_handle({"method": "tools/call", "params": {"name": "place_order", "arguments": {"basket": out["basket"]}}})
            print(f"[{step}] ORDER OK -> {res['content']}")
            msgs.append({"role": "tool", "content": json.dumps(res["content"])})
        else:
            print(f"[{step}] DONE"); return True
    return False

# ---- [LIFE] Life cycle: the spec doubles as the test (then monitor, iterate)
if __name__ == "__main__":
    print("tools:", [t["name"] for t in mcp_handle({"method": "tools/list"})["tools"]])
    assert run(), "acceptance test failed: bot never reached done_when"
    print("acceptance test passed ->", SPEC["done_when"])
