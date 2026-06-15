import helpers as h
import datamodels as dm

#                   LinkedIn scraper 
async def scrape(page, f):
    results = []
    try:
        kw = "%20".join(f.keywords) if f.keywords else "internship"
        loc = (f.location or "India").replace(" ", "%20")
        url = (f"https://www.linkedin.com/jobs/search/"
               f"?keywords={kw}%20internship&location={loc}&f_E=1&f_jT=I")
        print(f"    {url}")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)
        cards = await page.query_selector_all(
            ".job-search-card, .jobs-search__results-list li, [class*='job-card']"
        )
        print(f"    -> {len(cards)} cards")
        for card in cards[:30]:
            try:
                title = await h.txt(await card.query_selector("h3, .job-search-card-title"))
                if len(title) < 3: continue
                company = await h.txt(await card.query_selector(".job-search-card_company-name, h4"))
                
                href = await h.attr(await card.query_selector("a[href*='/jobs/']"), "href")
                loc_t = await h.txt(await card.query_selector(".job-search-card_location"))
                posted =  await h.txt(await card.query_selector("time"))
                mode_t = "Remote" if "remote" in loc_t.lower() else "On-site/Hybrid"
                results.append(dm.Internship(title=title, company=company,
                    platform="LinkedIn", url=href, location=loc_t, mode=mode_t, posted=posted))
                
            except: continue
    except Exception as e: print(f"     LinkedIn error: {e}")
    return results
        