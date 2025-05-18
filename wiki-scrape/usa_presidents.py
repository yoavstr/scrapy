import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"

response = requests.get(url)
response.raise_for_status()
html_content = response.text

soup = BeautifulSoup(html_content, "lxml")

table = soup.find_all("table", class_="wikitable sortable sticky-header")[0]
rows = table.find("tbody").find_all("tr")

table_caption = table.find("caption").text
print(table_caption)


def clean_vice_pres_text(text):
    # Remove bracketed content **along with any preceding spaces/commas**
    text = re.sub(r"(,\s*)?\[[^\]]*\]", "", text)

    # Add space in PascalCase (e.g., VacantAfter → Vacant After)
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)

    # Clean up extra whitespace and stray commas
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r",\s*,", ",", text)  # fix double commas
    text = re.sub(r"\s+,", ",", text)  # trim space before commas
    return re.sub(r",\s+", ", ", text)  # ensure proper comma spacing


def extract_years(s):
    s = s.strip("()").strip()

    # Case 1: birth–death years like "1732–1799"
    if re.match(r"^\d{4}[–-]\d{4}$", s):
        start, end = re.split(r"[–-]", s)
        return int(start), int(end)

    # Case 2: birth only like "b. 1946"
    match = re.match(r"^b\.\s*(\d{4})$", s, re.IGNORECASE)
    if match:
        start = int(match.group(1))
        end = "alive"
        return start, end

    # Fallback
    raise ValueError(f"Unrecognized format: {s}")


US_PRESIDENTS = []

for num_of_pres, president in enumerate(rows[1:], start=1):
    print("-----")
    info = president.find_all("td")
    birth_death = info[1].find("span").text
    # Remove brackets, Split on en dash or regular dash
    birth_year, death_year = extract_years(birth_death)

    name = info[1].find("b").find("a").text

    wiki_url = "https://en.wikipedia.org" + info[1].find("b").find("a").get("href")

    term = info[2].find_all("span")
    # term end is term start of next president
    term_start = term[0].text

    party = info[4].find("i").text if info[4].find("i") else info[4].find("a").text

    elections = info[5].find_all("a")
    if len(elections) == 0:
        election_year = "No Elections Held"
    elif len(elections) == 1:
        election_year = elections[0].text
    else:
        years = [year.text for year in elections]
        election_year = ", ".join(years)

    vice = info[6]
    if vice.find("hr"):
        vice_president = ", ".join([vice.text for vice in vice.find_all("a")])
    elif vice.find("i"):
        vice_president = vice.find("i").text
    elif vice.find("a"):
        vice_presidents = vice.find_all("a")
        vice_president = ", ".join([vice.text for vice in vice_presidents])
    vice_president_cleaned = clean_vice_pres_text(vice_president)

    response = requests.get(wiki_url)
    response.raise_for_status()
    html_content = response.text
    soup = BeautifulSoup(html_content, "lxml")
    # Cache the target div and paragraphs
    content_div = soup.find("div", class_="mw-content-ltr mw-parser-output").find_all("p")

    # Try paragraphs 1, 2, 3 in order, using a loop
    large_text = ""
    for i in [1, 2, 3]:
        if i < len(content_div):
            text = content_div[i].get_text(strip=True)
            if text:
                large_text = text
                break
    time.sleep(1)

    us_president_info = {
        "president_count": num_of_pres,
        "birth_year": birth_year,
        "death_year": death_year,
        "name": name,
        "party": party,
        "wiki_url": wiki_url,
        "term_start_date": term_start,
        "election_year": election_year,
        "vice_presidents": vice_president_cleaned,
        "description": large_text,
    }

    print(f"Extracted info for {num_of_pres}th President - {name}")

    US_PRESIDENTS.append(us_president_info)

df = pd.DataFrame(US_PRESIDENTS)
print(df)
