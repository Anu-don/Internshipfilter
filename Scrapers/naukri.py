import helpers as h, datamodels as dm

#                Naukri
async def scrape(page, f):
    results = []
    try:
        kw  = "-".join(f.keywords) if f.keywords else "internship"
        url = f"https://www.naukri.com/{kw}-internship-jobs"
        print(f"    {url}")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        cards = await page.query_selector_all(
            ".jobTuple, article.jobTupleHeader, [class*='srp-jobtuple']")
        print(f"    -> {len(cards)} cards")
        for card in cards[:30]:
            try:
                title    = await h.txt(await card.query_selector("a.title, [class*='title']"))
                if len(title) < 3: continue
                company  = await h.txt(await card.query_selector(".companyInfo a"))
                href     = await h.attr(await card.query_selector("a.title"), "href")
                location = await h.txt(await card.query_selector(".location, [class*='location']"))
                duration = await h.txt(await card.query_selector(".experience, [class*='experience']"))
                results.append(dm.Internship(title=title, company=company, platform="Naukri Campus",
                    url=href, location=location, duration=duration))
            except: continue
    except Exception as e: print(f"    Naukri error: {e}")
    return results
