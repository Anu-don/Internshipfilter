import helpers as h
import datamodels as dm

#               Indeed India
async def scrape(page, f):
    results = []
    try:
        kw  = "+".join(f.keywords) if f.keywords else "internship"
        loc = (f.location or "India").replace(" ","+")
        url = f"https://in.indeed.com/jobs?q={kw}+internship&l={loc}"
        print(f"    {url}")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        cards = await page.query_selector_all(
            ".job_seen_beacon, .jobsearch-ResultsList li")
        print(f"    -> {len(cards)} cards")
        for card in cards[:30]:
            try:
                title   = await h.txt(await card.query_selector("h2 a, .jobTitle"))
                if len(title) < 3: continue
                company = await h.txt(await card.query_selector("[class*='companyName']"))
                href    = await h.attr(await card.query_selector("a[href*='/pagead/'],a[href*='/rc/']"), "href")
                full_url = f"https://in.indeed.com{href}" if href.startswith("/") else href
                location = await h.txt(await card.query_selector("[class*='companyLocation']"))
                stipend  = await h.txt(await card.query_selector("[class*='salary']"))
                posted   = await h.txt(await card.query_selector("[class*='date']"))
                results.append(dm.Internship(title=title, company=company, platform="Indeed India",
                    url=full_url, location=location, stipend=stipend, posted=posted))
            except: continue
    except Exception as e: print(f"    Indeed error: {e}")
    return results
