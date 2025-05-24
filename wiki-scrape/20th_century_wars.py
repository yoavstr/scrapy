import re
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup


def clean_wikipedia_text(text: str) -> str:
    """
    Cleans Wikipedia paragraph text by removing citation markers, page references,
    excessive whitespace, and fixing spacing before punctuation.
    """
    # Remove reference markers like [1], [note 1], etc.
    text = re.sub(r"\[\s*.*?\s*\]", "", text)
    text = re.sub(r"\[note \d+\]", "", text, flags=re.IGNORECASE)
    # Remove page references like : p.5 or : p.189–190
    text = re.sub(r":\s* ?p\.\d+([–-]\d+)?", "", text)
    # Remove extra spaces before punctuation including closing parentheses
    text = re.sub(r"\s+([.,;:!?)])", r"\1", text)
    # Normalize whitespace
    return re.sub(r"\s+", " ", text).strip()


url = "https://en.wikipedia.org/wiki/Lists_of_wars_in_the_20th_century"

response = requests.get(url)
response.raise_for_status()
html_content = response.text

soup = BeautifulSoup(html_content, "lxml")

lists_of_wars = soup.find("div", class_="mw-content-ltr mw-parser-output").find_all("li")

war_lst = []

for indx, lst in enumerate(lists_of_wars, start=1):
    print(f"Now accessing link {indx}...")
    # Get link for each list
    war_list_url = "https://en.wikipedia.org" + lst.a["href"]
    response = requests.get(war_list_url)
    sleep(1)

    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, "lxml")
    all_tables = soup.find_all("table", class_="wikitable")
    for idx, table in enumerate(all_tables, start=1):
        print(f"Now scraping table {idx}...")
        table_body = table.find("tbody")
        all_wars = table_body.find_all("tr")
        for war_num, war in enumerate(all_wars):
            print(f"{war_num} wars have been scraped")
            if war.find("td"):
                war_info = war.find_all("td")
                war_started = war_info[0].get_text(strip=True)
                war_ended = war_info[1].get_text(strip=True)
                name_of_conflict = war_info[2].get_text(" ", strip=True)
                # Remove footnotes [6], no double whitespaces
                name_of_conflict_cleaned = s = re.sub(
                    r"\s+", " ", re.sub(r"\[\s*\d+\s*\]", "", name_of_conflict)
                ).strip()
                victorious_pary = name_of_conflict = war_info[3].get_text(", ", strip=True)
                defeated_party = war_info[4].get_text(", ", strip=True)

                # Get description of war
                if war_info[2].find("a"):
                    war_wiki_url = "https://en.wikipedia.org" + war_info[2].find("a").get("href")
                    war_wiki_url = war_wiki_url.split("#")[0].rstrip()

                # If no link in wikipedia index
                not_found = 404
                if ("index.php?" in war_wiki_url) or (response.status_code == not_found):
                    war_description = "No Wikipedia Page for this War"
                else:
                    response = requests.get(war_wiki_url)
                    sleep(1)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, "lxml")
                    # Cache the target div and paragraphs
                    content_div = soup.find(
                        "div", class_="mw-content-ltr mw-parser-output"
                    ).find_all("p")

                    # Try paragraphs in order, using a loop
                    war_description = ""
                    for i in range(10):
                        if i < len(content_div):
                            text = content_div[i].get_text(" ", strip=True)
                            min_text_length = 60
                            if len(text) > min_text_length:
                                war_description = text
                                break
                clean_war_description = clean_wikipedia_text(war_description)

                war_dict = {
                    "started": war_started,
                    "ended": war_ended,
                    "name_of_conflict": name_of_conflict,
                    "victorious_pary": victorious_pary,
                    "defeated_party": defeated_party,
                    "war_description": clean_war_description,
                    "war_number": war_num,
                }
                war_lst.append(war_dict)


final_wars_df = pd.DataFrame(war_lst)
print(final_wars_df)
