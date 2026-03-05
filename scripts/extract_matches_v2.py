import asyncio
import json
import re
from playwright.async_api import async_playwright

def format_date(date_text):
    """Convert ESPN date format to DD/MM/YYYY"""
    months_es = {
        'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04', 'may': '05', 'jun': '06',
        'jul': '07', 'ago': '08', 'sept': '09', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'
    }
    
    try:
        # Handle formats like "Dom, 6 Mar" or "6 Mar"
        parts = date_text.lower().replace(',', '').split()
        for i, part in enumerate(parts):
            if part in months_es:
                day = parts[i-1] if i > 0 else '01'
                month = months_es[part]
                return f"{day.zfill(2)}/{month}/2022"
    except:
        pass
    return date_text

def get_result(home_score, away_score, is_independiente_home):
    """Determine WIN/LOSS/DRAW from Independiente's perspective"""
    try:
        home = int(home_score)
        away = int(away_score)
        
        if home == away:
            return 'DRAW'
        
        if is_independiente_home:
            return 'WIN' if home > away else 'LOSS'
        else:
            return 'WIN' if away > home else 'LOSS'
    except:
        return 'DRAW'

async def extract_matches():
    matches = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        print("Navigating to ESPN...")
        await page.goto('https://www.espn.com.ar/futbol/equipo/resultados/_/id/11/temporada/2022', wait_until='networkidle')
        await asyncio.sleep(5)  # Wait for JavaScript to render
        
        print("Extracting match data...")
        
        # Scroll and load all matches
        scroll_count = 0
        max_scrolls = 30
        
        while scroll_count < max_scrolls:
            # Extract current visible matches
            new_matches = await page.evaluate('''() => {
                const matches = [];
                
                // ESPN uses various class patterns for match rows
                const selectors = [
                    '[class*="ScoreCell"]',
                    '[class*="Gamestrip"]',
                    '[class*="game"]',
                    'article',
                    'tr'
                ];
                
                for (const selector of selectors) {
                    const elements = document.querySelectorAll(selector);
                    for (const el of elements) {
                        const text = el.innerText;
                        // Look for patterns like "Independiente vs" or "vs Independiente"
                        if (text.includes('Independiente') && (text.includes('-') || text.includes('vs'))) {
                            matches.push({
                                selector: selector,
                                text: text,
                                html: el.outerHTML.substring(0, 500)
                            });
                        }
                    }
                }
                
                return matches;
            }''')
            
            if new_matches:
                print(f"Found {len(new_matches)} potential matches on scroll {scroll_count + 1}")
            
            # Try to click "Ver más" or scroll
            has_more = await page.evaluate('''() => {
                const buttons = Array.from(document.querySelectorAll('button, a'));
                const loadMore = buttons.find(b => 
                    b.innerText.toLowerCase().includes('ver más') ||
                    b.innerText.toLowerCase().includes('ver mas') ||
                    b.innerText.toLowerCase().includes('load more') ||
                    b.innerText.toLowerCase().includes('show more')
                );
                if (loadMore) {
                    loadMore.click();
                    return true;
                }
                return false;
            }''')
            
            if has_more:
                await asyncio.sleep(2)
            else:
                # Scroll down
                await page.evaluate('window.scrollBy(0, window.innerHeight)')
                await asyncio.sleep(1)
            
            scroll_count += 1
        
        # Final extraction
        print("\nDoing final extraction...")
        page_content = await page.content()
        
        # Save for inspection
        with open('/Users/fsodano/fibradev/historia-roja/data/page_final.html', 'w', encoding='utf-8') as f:
            f.write(page_content)
        
        # Extract structured data
        structured_matches = await page.evaluate('''() => {
            const results = [];
            
            // Get all text that might contain match info
            const bodyText = document.body.innerText;
            
            // Look for match patterns
            // ESPN typically shows: "Dom, 6 Mar" followed by team names and scores
            const lines = bodyText.split('\\n').map(l => l.trim()).filter(l => l);
            
            return {
                totalLines: lines.length,
                sampleLines: lines.slice(0, 100),
                bodyPreview: bodyText.substring(0, 3000)
            };
        }''')
        
        print(f"\nBody preview:\n{structured_matches['bodyPreview'][:2000]}")
        
        await browser.close()
        
        return matches

if __name__ == '__main__':
    matches = asyncio.run(extract_matches())
    print(f"\nExtraction complete!")
