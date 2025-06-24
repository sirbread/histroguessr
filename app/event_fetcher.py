import requests
from bs4 import BeautifulSoup
import re
import random

EVENTS = [
    "Chernobyl_disaster",
    "Fall_of_the_Berlin_Wall",
    "Assassination_of_John_F._Kennedy",
    "Sinking_of_the_Titanic",
    "Storming_of_the_Bastille",
    "September_11_attacks",
    "Great_Fire_of_London",
    "Apollo_11",
    "Battle_of_Hastings",
    "Attack_on_Pearl_Harbor",
    "United_States_Declaration_of_Independence",
    "Rwandan_genocide",
    "Columbine_High_School_massacre",
    "Magna_Carta",
    "French_Revolution"
]

YEAR_PATTERN = re.compile(r'(?<!\d)(1[0-9]{3}|20[0-2][0-9]|2025)(?!\d)')
DATE_RANGE_PATTERN = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\s*[-–]\s*(1[0-9]{3}|20[0-2][0-9])\b')

REMOVE_SECTIONS = [
    "References",
    "External links",
    "See also",
    "Further reading",
    "Notes",
    "Bibliography"
]

def fetch_full_redacted_event():
    title = random.choice(EVENTS)
    url = f"https://en.wikipedia.org/api/rest_v1/page/html/{title}"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        for heading in soup.find_all(["h2", "h3", "h4"]):
            heading_text = heading.get_text(strip=True)
            for unwanted in REMOVE_SECTIONS:
                if unwanted in heading_text:
                    next_node = heading.find_next_sibling()
                    while next_node and not (next_node.name and next_node.name.startswith("h") and int(next_node.name[1]) <= int(heading.name[1])):
                        temp = next_node.find_next_sibling()
                        next_node.decompose()
                        next_node = temp
                    heading.decompose()
                    break

        actual_year = None
        for text_node in soup.find_all(string=True):
            parent = text_node.parent.name
            if parent not in ["script", "style"] and len(text_node.strip()) > 0:
                if actual_year is None:
                    match = YEAR_PATTERN.search(text_node)
                    if match:
                        actual_year = int(match.group())

        for text_node in soup.find_all(string=True):
            parent = text_node.parent.name
            if parent not in ["script", "style"] and len(text_node.strip()) > 0:
                redacted = YEAR_PATTERN.sub("████", text_node)
                redacted = DATE_RANGE_PATTERN.sub("████–████", redacted)
                text_node.replace_with(redacted)

        return {
            "title": title.replace("_", " "),
            "html": str(soup),
            "answer": actual_year
        }
    except Exception as e:
        print(f"[error] failed to load {title} -> {e}")
        return None

