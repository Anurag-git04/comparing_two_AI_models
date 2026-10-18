"""
Call 3 models (1 Gemini + 2 Groq) with the same prompt and log
latency, time-to-first-token (TTFT) and token counts in a table.

Setup:
    pip install groq google-genai
    export GROQ_API_KEY=...
    export GEMINI_API_KEY=...

Run:
    python compare_models.py
    python compare_models.py "Your own prompt here"
"""

import os
import sys
import time

from dotenv import load_dotenv
from groq import Groq
from google import genai

load_dotenv()

PROMPT = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "Explain how a hash map works in about 150 words."
)

# Change these if a model is renamed/retired.
# GROQ_MODELS = ["llama-3.3-70b-versatile", "openai/gpt-oss-20b"]
# GEMINI_MODEL = "gemini-2.5-flash"
GROQ_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
GEMINI_MODEL = "gemini-3.8-flash"

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def call_groq(model: str) -> dict:
    start = time.perf_counter()
    ttft = None
    text = []
    usage = None

    stream = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            if ttft is None:
                ttft = time.perf_counter() - start
            text.append(chunk.choices[0].delta.content)
        # Usage arrives on the final chunk (location differs by SDK version).
        u = getattr(chunk, "usage", None)
        if u is None and getattr(chunk, "x_groq", None) is not None:
            u = getattr(chunk.x_groq, "usage", None)
        if u is not None:
            usage = u

    latency = time.perf_counter() - start
    return {
        "provider": "Groq",
        "model": model,
        "ttft": ttft,
        "latency": latency,
        "in_tok": getattr(usage, "prompt_tokens", None),
        "out_tok": getattr(usage, "completion_tokens", None),
        "total_tok": getattr(usage, "total_tokens", None),
        "text": "".join(text),
    }

def with_retry(fn, model, tries=4, wait=3):
    for attempt in range(1, tries + 1):
        try:
            return fn(model)
        except Exception as e:
            if attempt == tries or "503" not in str(e):
                raise
            print(f"[retry {attempt}] {model}: {e}", file=sys.stderr)
            time.sleep(wait * attempt)

def call_gemini(model: str) -> dict:
    start = time.perf_counter()
    ttft = None
    text = []
    usage = None

    for chunk in gemini_client.models.generate_content_stream(
        model=model, contents=PROMPT
    ):
        if chunk.text:
            if ttft is None:
                ttft = time.perf_counter() - start
            text.append(chunk.text)
        if chunk.usage_metadata is not None:
            usage = chunk.usage_metadata

    latency = time.perf_counter() - start
    out_tok = None
    if usage is not None:
        # Include "thinking" tokens, which are billed as output.
        out_tok = (usage.candidates_token_count or 0) + (
            getattr(usage, "thoughts_token_count", 0) or 0
        )
    return {
        "provider": "Gemini",
        "model": model,
        "ttft": ttft,
        "latency": latency,
        "in_tok": getattr(usage, "prompt_token_count", None),
        "out_tok": out_tok,
        "total_tok": getattr(usage, "total_token_count", None),
        "text": "".join(text),
    }


def fmt(v, spec=""):
    return "-" if v is None else format(v, spec)


def main():
    jobs = [(call_groq, m) for m in GROQ_MODELS] + [(call_gemini, GEMINI_MODEL)]
    results = []
    for fn, model in jobs:
        try:
            # results.append(fn(model))
            results.append(with_retry(fn, model))
        except Exception as e:  # keep going if one provider fails
            print(f"[error] {model}: {e}", file=sys.stderr)

    headers = ["Provider", "Model", "TTFT (s)", "Latency (s)",
               "In tok", "Out tok", "Total tok", "Out tok/s"]
    rows = []
    for r in results:
        gen_time = (r["latency"] - r["ttft"]) if r["ttft"] else None
        tps = (r["out_tok"] / gen_time) if (r["out_tok"] and gen_time) else None
        rows.append([
            r["provider"], r["model"], fmt(r["ttft"], ".3f"),
            fmt(r["latency"], ".3f"), fmt(r["in_tok"]), fmt(r["out_tok"]),
            fmt(r["total_tok"]), fmt(tps, ".1f"),
        ])

    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    def row(cells):
        return "| " + " | ".join(str(c).ljust(w) for c, w in zip(cells, widths)) + " |"

    print(f"\nPrompt: {PROMPT}\n")
    print(line); print(row(headers)); print(line)
    for r_ in rows:
        print(row(r_))
    print(line)

    # Also save the table + outputs for later reference.
    with open("results.md", "w", encoding="utf-8") as f:
        f.write(f"Prompt: {PROMPT}\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("|" + "---|" * len(headers) + "\n")
        for r_ in rows:
            f.write("| " + " | ".join(r_) + " |\n")
        for r in results:
            f.write(f"\n## {r['model']}\n\n{r['text']}\n")
    print("\nSaved results.md")


if __name__ == "__main__":
    main()