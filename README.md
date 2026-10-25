# 🤖 Agent Concepts PoC: A Grocery Bot and its Harness

[![Deploy static content to Pages](https://github.com/rifaterdemsahin/agent-concepts-to-learn-for-development/actions/workflows/static.yml/badge.svg)](https://github.com/rifaterdemsahin/agent-concepts-to-learn-for-development/actions/workflows/static.yml)

🌐 **Live Documentation & Interactive Concept Map**:  
👉 **[https://rifaterdemsahin.github.io/agent-concepts-to-learn-for-development/](https://rifaterdemsahin.github.io/agent-concepts-to-learn-for-development/)**

Learn linked core concepts by running one self-contained, zero-dependency reference bot. No API key needed; the model is mocked.

```bash
python poc/bot.py        # runs the bot and its acceptance test
open index.html          # interactive concept map
```

---

## 📚 Complete Concept Pages (with Top Infographics & Emojis)

| Page | Concept | Key Takeaway |
|---|---|---|
| [index.html](index.html) | 🗺️ Interactive Concept Map | Overview graph connecting all concepts |
| [first-principles.html](first-principles.html) | ⚛️ First Principles | Deconstructing agency, stochasticity, and deterministic harnesses |
| [sanity-check.html](sanity-check.html) | 🔬 Sanity Check & Guardrails | Zero-trust validation, bounds checking, and failure prevention |
| [timeline.html](timeline.html) | ⏳ Numbered Timeline of Events | 12-stage chronological lifecycle from spec to production |
| [requirements.html](requirements.html) | 📋 Understanding Requirements | `SPEC` dict becomes prompt, validator rules, and acceptance test |
| [architecture.html](architecture.html) | 🏗️ Agent Architecture | Bounded `run()` loop wrapping a stateless model |
| [llm.html](llm.html) | 🧠 LLM Fundamentals | Stateless model, harness memory, token budgeting |
| [output.html](output.html) | 🛡️ Output Handling | Regex extraction, business validation, retry error loops |
| [mcp.html](mcp.html) | 🔌 MCP Development | Standard `tools/list` and `tools/call` JSON-RPC protocol interface |
| [lifecycle.html](lifecycle.html) | 🔄 Systems Life Cycle | Spec, build, test, deploy, monitor, iterate in a closed loop |

---

## 🔗 How Concepts Map to `poc/bot.py`

| Concept | Tag & Location in `poc/bot.py` | Role in Agentic Flow |
|---|---|---|
| 📋 Requirements | `[REQ]` `SPEC` dict | Single source of truth driving prompt, rules, and acceptance test |
| 🔌 MCP Protocol | `[MCP]` `mcp_handle()` | Protocol boundary providing standard tool discovery and calls |
| 🧠 LLM Fundamentals | `[LLM]` `mock_llm()`, `tokens()` | Stateless text transformer; context window accounting |
| 🛡️ Output Handling | `[OUT]` `parse()`, `validate()` | First basket under £50 rejected; error fed back for retry |
| 🏗️ Architecture | `[ARCH]` `run()` loop | Bounded coordination loop connecting model, validation, and tools |
| 🔬 Sanity Checking | Multiple locations | Hard token caps, JSON regex extraction, schema checks, max steps |
| 🔄 Systems Life Cycle | `[LIFE]` `__main__` assert | Automated acceptance gate; monitoring feeds future requirements |

---

## 🧪 Quick Test & Exercises

Run the test suite:
```bash
python poc/bot.py
```

Expected output:
```text
tools: ['list_pantry', 'place_order']
[0] tool list_pantry -> {'milk': 0, 'eggs': 2, 'rice': 1, 'yoghurt': 0}
[1] REJECTED: basket £10.2 is below minimum £50
[2] ORDER OK -> {'status': 'order_placed', 'total': 50.6}
[3] DONE
acceptance test passed -> order_placed
```

### Exercises
1. Change `min_basket_gbp` to 80 and watch the retry loop fail at `max_steps`.
2. Add a `get_prices` tool and expose it strictly through `mcp_handle`.
3. Swap `mock_llm` for a live model API; keep `parse`/`validate` completely unchanged.
4. Add per-step logging (monitor stage) and formulate one new requirement in `SPEC` based on telemetry.
