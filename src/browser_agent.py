#!/usr/bin/env python3
"""
browser_agent.py - Enterprise Visual Computer-Use Browser Agent
Powered by browser-use (36k+ stars) & Google Chrome Headless.
Integrates directly into the Nod Chief of Staff WhatsApp Loop.
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Load Hermes environment for API keys
ENV_PATHS = [
    "/home/ubuntu/.hermes/.env",
    os.path.expanduser("~/.hermes/.env")
]

def load_env():
    env = {}
    for p in ENV_PATHS:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
            if env:
                break
    return env

ENV = load_env()
GEMINI_API_KEY = ENV.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

async def run_browser_task(task: str, headless: bool = True):
    print(f"[*] Initializing browser-use Agent for task: '{task}'")
    try:
        from browser_use import Agent
        from browser_use.browser.browser import Browser, BrowserConfig
        from langchain_google_genai import ChatGoogleGenerativeAI

        if not GEMINI_API_KEY:
            raise ValueError("Missing GEMINI_API_KEY in ~/.hermes/.env")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.1
        )

        browser = Browser(
            config=BrowserConfig(
                headless=headless,
                chrome_instance_path="/usr/bin/google-chrome",
                extra_chromium_args=[
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-dev-shm-usage"
                ]
            )
        )

        agent = Agent(
            task=task,
            llm=llm,
            browser=browser
        )

        history = await agent.run(max_steps=10)
        final_result = history.final_result()
        print(f"[+] Task Completed Successfully. Result:\n{final_result}")
        return {"success": True, "result": final_result}

    except Exception as e:
        print(f"[ERROR] browser-use execution failed: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    task_input = sys.argv[1] if len(sys.argv) > 1 else "Go to https://amz34.github.io/dev-requisition/ and verify the top header ribbon text and buttons."
    res = asyncio.run(run_browser_task(task_input, headless=True))
    print(json.dumps(res, indent=2))
