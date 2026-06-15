import helpers as h, datamodels as dm

#                   UnStop
async def scrape(page, f):
    results = []
    try:
        kw  = "%20".join(f.keywords) if f.keywords else ""
        url = f"https://unstop.com/internships?searchTerm={kw}"
        print(f"    {url}")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)
        for _ in range(3):
            await page.keyboard.press("End")
            await page.wait_for_timeout(1200)
        cards = await page.query_selector_all(
            "[class*='opportunity'], [class*='listing-card'], app-card")
        print(f"    -> {len(cards)} cards")
        for card in cards[:30]:
            try:
                title = await h.txt(await card.query_selector("h2,h3,[class*='title'],[class*='name']"))
                if len(title) < 3: continue
                company  = await h.txt(await card.query_selector("[class*='company']"))
                link_el  = await card.query_selector("a")
                href     = await h.attr(link_el, "href")
                full_url = f"https://unstop.com{href}" if href.startswith("/") else href
                stipend  = await h.txt(await card.query_selector("[class*='stipend'],[class*='salary']"))
                location = await h.txt(await card.query_selector("[class*='location']"))
                deadline = await h.txt(await card.query_selector("[class*='deadline'],[class*='date']"))
                tag_els  = await card.query_selector_all("[class*='tag'],[class*='chip']")
                skills   = [await h.txt(t) for t in tag_els[:5]]
                skills   = [s for s in skills if s]
                results.append(dm.Internship(title=title, company=company, platform="Unstop",
                    url=full_url, location=location, stipend=stipend,
                    deadline=deadline, skills=skills))
            except: continue
    except Exception as e: print(f"    Unstop error: {e}")
    return results

