# Agent concepts PoC: a grocery bot and its harness

Learn six linked concepts by running one small bot. No API key; the model is mocked.

```
python poc/bot.py        # runs the bot and its acceptance test
open index.html          # interactive concept map (enable GitHub Pages on main / root)
```

| Concept | Where in `poc/bot.py` | Links to |
|---|---|---|
| Understanding requirements | `SPEC` | becomes the prompt, the validator rules and the acceptance test |
| Agent architecture | `run()` loop | calls the LLM, gates output, routes tools |
| LLM fundamentals | `mock_llm()`, `tokens()` | stateless, so the harness holds memory; free text, so output needs handling |
| Output handling | `parse()`, `validate()` | first basket is under £50, rejected, error fed back, model retries |
| MCP dev | `mcp_handle()` | `tools/list` and `tools/call` give the loop a standard tool interface |
| Systems life cycle | `__main__` assert | spec, build, test, deploy, monitor, iterate; monitoring feeds new requirements |

## Exercises
1. Change `min_basket_gbp` to 80 and watch the retry loop fail at `max_steps`.
2. Add a `get_prices` tool and expose it only through `mcp_handle`.
3. Swap `mock_llm` for a real API call; keep `parse`/`validate` unchanged.
4. Add logging per step (monitor stage) and write one new requirement from what you see.
