import helpers as h

def apply_filters(internship, f):
    kept = []
    for i in internship:
        blob = " ".join([i.title, i.company, i.description,
                        i.domain, " ".join(i.skills), i.location]).lower()
        if f.keywords and not any(kw.lower() in blob for kw in f.keywords):
            continue
        if f.min_stipend and i.stipend:
            v = h.stipend_num(i.stipend)
            if v  and v < f.min_stipend: continue
        if f.location:
            loc = (i.location + " " + i.mode).lower()
            if f.location.lower() not in loc and "remote" not in loc:
                continue
            
        kept.append(i)
    print(f"    Filters: {len(kept)} kept / {len(internship) - len(kept)} dropped ")
    return kept

            