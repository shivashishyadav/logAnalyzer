"""Groq tool-calling agent loop: LLM decides which tool to call"""
import json
import os
from groq import Groq
from dotenv import load_dotenv
from tools import FUNCS, TOOL_SCHEMAS

load_dotenv() 

MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
SYSTEM = """Tum ek Network Operations assistant ho. Network logs ke issues dhoondhna,
root cause batana aur fix suggest karna tumhara kaam hai. Jawab dene se pehle tools use karo,
andaza mat lagao. Jawab simple Hindi ya English ya agar user bole to dono me do: problem, probable cause, suggested fix."""


def run_agent(user_msg, history=None, api_key=None, max_steps=6):
    client = Groq(api_key=api_key or os.environ["GROQ_API_KEY"])
    messages = [{"role": "system", "content": SYSTEM}] + (history or []) + [
        {"role": "user", "content": user_msg}]
    trace = []
    for _ in range(max_steps):
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOL_SCHEMAS, tool_choice="auto")
        msg = resp.choices[0].message
        if not msg.tool_calls:
            return msg.content, trace
        messages.append({"role": "assistant", "content": msg.content or "",
                         "tool_calls": [{"id": c.id, "type": "function",
                                         "function": {"name": c.function.name,
                                                      "arguments": c.function.arguments}}
                                        for c in msg.tool_calls]})
        for c in msg.tool_calls:
            args = json.loads(c.function.arguments or "{}")
            try:
                result = FUNCS[c.function.name](**args)
            except Exception as e:
                result = {"error": str(e)}
            trace.append((c.function.name, args, result))
            messages.append({"role": "tool", "tool_call_id": c.id,
                             "content": json.dumps(result)})
    return "Max steps reached, Try again!", trace


if __name__ == "__main__":
    ans, tr = run_agent(input("Question: "))
    for name, args, _ in tr:
        print(f"[tool] {name}({args})")
    print(ans)
