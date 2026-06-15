import helpers as h, datamodels as dm

#               WellFound
async def scrape(page, f):
    results = []
    try:
        kw = "%20".join(f.keywords) if f.keywords else ""
        url = f"https://wellfound.com/jobs?jobType=internship&q={kw}"
        print(f"    {url}")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)
        cards = await page.query_selector_all("[class*='JobListing'], article")
        print(f"        {url}")
        
        for card in cards[:30]:
            try:
                title = await h.txt(await card.query_selector("h2,h3,[class*='title']"))
                if len(title) < 3: continue
                company = await h.txt(await card.query_selector("[class*='startup'],[class*='company']"))
                href = await h.attr(await card.query_selector("[class*='compensation']"), "href")
                full_url = f"https://wellfound.com{href}" if href.startswith("/") else href
                location = await h.txt(await card.query_selector("[class*='location']"))
                stipend  = await h.txt(await card.query_selector("[class*='compensation']"))
                results.append(dm.Internship(title=title, company=company, platform="Wellfound",
                    url=full_url, location=location, stipend=stipend))
            except: continue
    except Exception as e: print(f" Wellfound error: {e}")
    return results
