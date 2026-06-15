from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Internship:
    title: str
    company: str
    platform: str
    url: str = ""
    location: str = ""
    mode: str = ""
    stipend: str = ""
    duration: str = ""
    domain: str = ""
    skills: list = field(default_factory=list)
    deadline: str = ""
    posted: str = ""
    description: str = ""
    
@dataclass
class Filters:
    keywords:  list = field(default_factory=list)
    domain: Optional[str] = None
    mode: Optional[str] = None              # "remote" | "Hybrid" | "Onsite"
    min_stipend: Optional[int] = None       # ₹/month
    location: Optional[str] = None
    max_duration: Optional[str] = None      # Months
    
    