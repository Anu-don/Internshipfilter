import datamodels, platform_registry

# ── MODE / FILTER PROMPTS ─────────────────────────────────────────────────────
def select_mode():
    print("\n" + "="*50)
    print("  INTERNSHIP SEARCH AUTOMATION")
    print("="*50)
    print("\n  [0] DEFAULT — auto-search Internshala + LinkedIn + Unstop")
    print("  [1] CUSTOM  — pick your own platform(s)\n")
    while True:
        c = input("  Enter 0 or 1: ").strip()
        if c in ("0","1"): return int(c)
        print("  Please enter 0 or 1")

def select_platforms():
    print("\n  Available Platforms:")
    for n, info in platform_registry.PLATFORMS.items():
        print(f"    [{n}] {info['name']}")
    print("\n  Enter numbers separated by commas  (e.g.  1,3  or  2)")
    while True:
        raw = input("  Your choice: ").strip()
        parts = [p.strip() for p in raw.split(",")]
        sel = []
        ok = True
        for p in parts:
            if p.isdigit() and int(p) in platform_registry.PLATFORMS: sel.append(int(p))
            else: print(f"  Invalid: {p}"); ok = False; break
        if ok and sel:
            print(f"  Selected: {', '.join(platform_registry.PLATFORMS[i]['name'] for i in sel)}")
            return sel

def collect_filters():
    print("\n" + "-"*50 + "\n  Filters  (Enter to skip any)\n" + "-"*50)
    f = datamodels.Filters()
    kw = input("  Keywords (e.g. python,ML,design): ").strip()
    if kw: f.keywords = [k.strip() for k in kw.split(",")]
    d  = input("  Domain (e.g. AI, Web Dev, Finance): ").strip()
    if d: f.domain = d
    m  = input("  Work mode [remote/hybrid/onsite]: ").strip().lower()
    if m in ("remote","hybrid","onsite"): f.mode = m
    s  = input("  Min stipend INR/month (e.g. 5000): ").strip()
    if s.isdigit(): f.min_stipend = int(s)
    l  = input("  Location (e.g. Bangalore): ").strip()
    if l: f.location = l
    return f
