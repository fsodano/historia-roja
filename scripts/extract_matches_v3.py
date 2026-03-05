import asyncio
import json
from playwright.async_api import async_playwright

async def extract_matches():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to ESPN...")
        await page.goto('https://www.espn.com.ar/futbol/equipo/resultados/_/id/11/temporada/2022')
        
        print("Waiting for content to load...")
        await asyncio.sleep(5)
        
        # Get all page text
        content = await page.content()
        
        with open('/Users/fsodano/fibradev/historia-roja/data/page_content.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved HTML, length: {len(content)}")
        
        # Get body text
        body_text = await page.inner_text('body')
        
        with open('/Users/fsodano/fibradev/historia-roja/data/body_text.txt', 'w', encoding='utf-8') as f:
            f.write(body_text)
        
        print(f"Saved body text, length: {len(body_text)}")
        print(f"Preview: {body_text[:1000]}")
        
        await browser.close()

asyncio.run(extract_matches())
