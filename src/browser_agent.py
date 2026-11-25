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

def get_llm():
    """Initializes LLM via local high-speed 8801 OpenAI-compatible gateway (Gemini 3.8 Flash) using Pydantic AI."""
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.models.openai import OpenAIChatModel

    provider = OpenAIProvider(
        base_url="http://127.0.0.1:8801/v1",
        api_key="sk-local-proxy"
    )
    return OpenAIChatModel("google/gemini-3.8-flash", provider=provider)

async def run_browser_task(task: str, headless: bool = True):
    print(f"[*] Initializing browser-use Agent for task: '{task}'")
    try:
        from browser_use import Agent, Browser

        llm = get_llm()

        browser = Browser(
            'chromium',
            executable_path="/usr/bin/google-chrome",
            headless=headless
        )

        agent = Agent(
            task=task,
            llm=llm,
            browser=browser
        )

        history = await agent.run(max_steps=5)
        final_result = history.final_result()
        print(f"[+] Task Completed Successfully. Result:\n{final_result}")
        return {"success": True, "result": final_result}

    except Exception as e:
        print(f"[ERROR] browser-use execution failed: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    task_input = sys.argv[1] if len(sys.argv) > 1 else "Go to https://amz34.github.io/dev-requisition/ and tell me the page header title."
    res = asyncio.run(run_browser_task(task_input, headless=True))
    print(json.dumps(res, indent=2))
