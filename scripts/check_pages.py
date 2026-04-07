#!/usr/bin/env python3
"""页面检查脚本 - 验证网站页面是否正常"""
import asyncio
from playwright.async_api import async_playwright

SITES = [
    ("index",    "https://xiaohuahua.vercel.app/index.html"),
    ("story",    "https://xiaohuahua.vercel.app/story.html"),
    ("bagua",    "https://xiaohuahua.vercel.app/bagua.html"),
    ("trading",  "https://xiaohuahua.vercel.app/trading.html"),
    ("diary",    "https://xiaohuahua.vercel.app/diary.html"),
]

async def check_page(browser, name, url):
    errors = []
    page = await browser.new_page()
    page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
    page.on("pageerror", lambda err: errors.append(f"[PAGE ERROR] {err}"))

    try:
        resp = await page.goto(url, wait_until="networkidle", timeout=20000)
        status = resp.status if resp else "?"
        title = await page.title()
        ok = "✅" if status == 200 else "⚠️"
        print(f"  {ok} {name:10s} | status:{status} | {title[:50]}")
    except Exception as e:
        print(f"  ❌ {name:10s} | {e}")
        await page.close()
        return

    if errors:
        for e in errors[:3]:
            print(f"     {e}")
    await page.close()

async def main():
    print("🔍 检查官网页面...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [check_page(browser, name, url) for name, url in SITES]
        await asyncio.gather(*tasks)
        await browser.close()
    print("✅ 检查完成")

if __name__ == "__main__":
    asyncio.run(main())
