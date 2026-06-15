'''
    ╔=============================================================╗
    ║           Internship Search Automation                      ║
    ║   Mode 0 -> Searches All Default platform.platforms automatically    ║
    ║   Mode 1 -> You choose which platform(s) to search          ║
    ╚=============================================================╝

Usage: 
    python app.py 
    python app.py --mode 0     # default mode 
    python app.py --mode 1     # Custom mode with input websites
    python app.py --output my_results.docx 
'''

import asyncio, argparse, json, re, sys, os
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

#scrape file 
import Scrapers.indeed as indeed, Scrapers.Internshala as internshala, Scrapers.linkedin as linkedin
import Scrapers.naukri as naukri, Scrapers.unstop as unstop, Scrapers.wellfound as wellfound
# Docx Generator 
import docxgenerator as docxg
from datetime import datetime
# other files
import platform_registry, filterengine, modefilter, helpers

SCRAPER_MAP = {
    'internshala': internshala.scrape,
    'linkedin': linkedin.scrape,
    'unstop': unstop.scrape,
    'indeed': indeed.scrape,
    'naukri': naukri.scrape,
    'wellfound': wellfound.scrape,
}


# ── MAIN ──────────────────────────────────────────────────────────────────────
async def run(mode, platform_ids, filters, output):
    names = [platform_registry.PLATFORMS[i]["name"] for i in platform_ids]
    keys  = [platform_registry.PLATFORMS[i]["key"]  for i in platform_ids]
    print(f"\nMode: {mode}  |  Platforms: {', '.join(names)}")
    all_results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(user_agent=helpers.UA, viewport={"width":1280,"height":900})
        for key, name in zip(keys, names):
            print(f"\n[{name}]")
            scraper = SCRAPER_MAP.get(key)
            if not scraper: print("  No scraper — skipping"); continue
            page = await ctx.new_page()
            items = await scraper(page, filters)
            print(f"  Scraped {len(items)}")
            all_results.extend(items)
            await page.close()
        await browser.close()
    # Dedup
    seen, unique = set(), []
    for i in all_results:
        k = (i.title.lower(), i.company.lower())
        if k not in seen: seen.add(k); unique.append(i)
    print(f"\nTotal unique: {len(unique)}")
    filtered = filterengine.apply_filters(unique, filters)
    if not filtered: print("No matches — showing all"); filtered = unique[:30]
    # Save JSON
    jp = output.replace(".docx",".json")
    with open(jp,"w") as jf: json.dump([i.__dict__ for i in filtered], jf, indent=2)
    print(f"  JSON -> {jp}")
    docxg.save_docx(filtered, filters, mode, names, output)
    print(f"\nDone! {len(filtered)} internships saved to {output}\n")

def main():
    if not os.path.exists("results"):
        os.makedirs("results")
    op = f"results/internship_results_{datetime.now().strftime('%Y-%m-%d')}.docx"
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",   type=int, choices=[0,1])
    parser.add_argument("--output", default=op)
    args = parser.parse_args()
    mode = args.mode if args.mode is not None else modefilter.select_mode()
    platform_ids = platform_registry.DEFAULT_PLATFORMS if mode == 0 else modefilter.select_platforms()
    filters = modefilter.collect_filters()
    asyncio.run(run(mode, platform_ids, filters, args.output))

if __name__ == "__main__":
    main()
