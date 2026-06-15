import asyncio
import sys
from playwright.async_api import async_playwright

# Configuration for supported websites
SITE_CONFIGS = {
    "linkedin": {
        "name": "LinkedIn",
        "url_template": "https://www.linkedin.com/jobs/search/?keywords={title}&location={location}&f_E=1",
        "selectors": {
            "card": ".base-card",
            "title": ".base-search-card__title",
            "company": ".base-search-card__subtitle",
            "link": "a.base-card__full-link"
        }
    },
    "indeed": {
        "name": "Indeed",
        "url_template": "https://www.indeed.com/jobs?q={title}+internship&l={location}",
        "selectors": {
            "card": ".job_seen_beacon",
            "title": "h2.jobsearch-JobInfoHeader-title", # Note: Indeed selectors change frequently
            "company": "[data-testid='company-name']",
            "link": "a.jcs-JobTitle"
        }
    }
}

async def run_automation():
    print("=== Multi-Site Internship Automation ===")
    
    # 1. Take Website Input
    print("\nSupported websites: linkedin, indeed")
    site_choice = input("Enter website to search (Example: linkedin): ").strip().lower()
    if site_choice not in SITE_CONFIGS:
        print(f"Site '{site_choice}' not specifically configured. Defaulting to LinkedIn.")
        site_choice = "linkedin"
    
    config = SITE_CONFIGS[site_choice]

    # 2. Take Topic/Title Input
    title_input = input("Enter job topic (Example: cyber security): ").strip()
    if not title_input:
        title_input = "cyber security"
        print(f"Defaulting to: {title_input}")

    # 3. Take Location Input
    location_input = input("Enter location (Example: New York or Remote): ").strip()
    if not location_input:
        location_input = "Remote"
        print(f"Defaulting to: {location_input}")

    async with async_playwright() as p:
        print(f"\n[1/3] Launching browser for {config['name']}...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # Build URL
        search_url = config['url_template'].format(
            title=title_input.replace(' ', '%20'),
            location=location_input.replace(' ', '%20')
        )
        
        print(f"[2/3] Navigating to: {search_url}")
        await page.goto(search_url)

        print("[3/3] Extracting results...")
        try:
            sel = config['selectors']
            # Wait for any of the job titles to load
            await page.wait_for_selector(sel['title'], timeout=10000)
            
            # Select job cards
            jobs = await page.query_selector_all(sel['card'])
            
            print(f"\nFound {len(jobs)} results for {title_input} in {location_input}:")
            print("=" * 60)

            for index, job in enumerate(jobs[:10]):
                title_el = await job.query_selector(sel['title'])
                company_el = await job.query_selector(sel['company'])
                link_el = await job.query_selector(sel['link'])
                
                title = (await title_el.inner_text()).strip() if title_el else "N/A"
                company = (await company_el.inner_text()).strip() if company_el else "N/A"
                link = await link_el.get_attribute("href") if link_el else "#"
                
                # Ensure absolute URL
                if link.startswith('/'):
                    if site_choice == "linkedin": link = "https://www.linkedin.com" + link
                    if site_choice == "indeed": link = "https://www.indeed.com" + link

                print(f"{index + 1}. {title}")
                print(f"   Company: {company}")
                print(f"   Link:    {link.split('?')[0]}")
                print("-" * 30)

        except Exception as e:
            print("\n[!] Error: No results found or page blocked by bot detection.")
            print(f"Details: {e}")
            await page.screenshot(path=f"error_{site_choice}.png")

        print("\nPress Enter to close the browser.")
        input()
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(run_automation())
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(0)
