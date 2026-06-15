import helpers as h
import datamodels as dm


#                   Scrapers 
async def scrape(page, f):
    results = []
    try:
        kw = "+".join(f.keywords) if f.keywords else "internship"
        url = (f"https://internshala.com/internship/work-from-home-{kw}-internship"
               if f.mode and "remote" in f.mode
               else f"https://internshala.com/internships/{kw}-internship")
        
        print(f"    {url}")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        try: await page.click("button:has-text('Accept')", timeout=2000)
        except: pass
        
        cards = await page.query_selector_all(
            ".internship_meta, .individual_internship, "
            "#internship_list_container .internship_list_container_1")
        print(f"     -> {len(cards)} cards")
        
        for card in cards:
            try:
                title_el = await card.query_selector(
                    ".job-internship-name, h3, [class*='profile']")
                title = await h.txt(title_el)
                if len(title) < 3: continue
                
                company = await h.txt(await card.query_selector(".company_name, [class*='company']"))
                link_el = await card.query_selector("a")
                href =  await h.attr(link_el, "href")
                
                full_url = f"https://internshala.com{href}" if href.startswith("/") else href
                stipend  = await h.txt(await card.query_selector(".stipend, [class*='stipend']"))
                duration = await h.txt(await card.query_selector(".duration, [class*='duration']"))
                location = await h.txt(await card.query_selector(".location_names, [class*='location']"))
                posted   = await h.txt(await card.query_selector("[class*='posted']"))

                mode_t   = "Remote" if "work from home" in location.lower() else location
                
                results.append(dm.Internship(title=title, company=company, platform="Internshala",
                                          url=full_url, location=location, mode=mode_t, 
                                          stipend=stipend, duration=duration, posted=posted))
            except: continue
            
    except Exception as e: print(f"     Internshala Error: {e}")
    return results
