from playwright.async_api import async_playwright
import re

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

async def txt(el):
    try: return (await el.inner_text()).strip() if el else ""
    except: return ""
    
async def attr(el, a):
    try: return (await el.get_attribute(a) or "").strip() if el else ""
    except: return ""
    
def stipend_num(s):
    nums = re.findall(r"[\d,]+", s.replace(",",""))
    if not nums: return 0
    v = int(nums[0])
    if "lakh" in s.lower(): v *= 100_000
    elif "k" in s.lower(): v *= 1_000
    return v


