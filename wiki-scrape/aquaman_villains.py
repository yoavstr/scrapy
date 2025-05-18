from bs4 import BeautifulSoup
import requests
from collections import Counter
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_Aquaman_enemies"

response = requests.get(url)
response.raise_for_status()
html_content = response.text

soup = BeautifulSoup(html_content, "lxml")

table = soup.find_all("table", class_="wikitable plainrowheaders sortable defaultcenter")[0]
rows = table.find("tbody").find_all("tr")

aquaman_villains = []

for row in rows[1:]:
    th = row.find("th")
    if th:
        # Get text content regardless of tags inside <th>
        villain = th.get_text(strip=True)

    td = row.find_all("td")
    first_appearance = td[0].get_text(strip=True)
    description = td[1].get_text(strip=True)

    info = {"villain": villain,
            "first_appearance": first_appearance,
            "description": description}

    aquaman_villains.append(info)

# Cleaning duplicates and text
all_villains = [item["villain"] for item in aquaman_villains]

# Use Counter to count the occurrences of each element in the list
counts = Counter(all_villains)
duplicates = [item for item, count in counts.items() if count > 1]

# Replacement names
replacements = {
    "Black MantaDavid Hyde[a]": "Black Manta (David Hyde)",
    "Ocean MasterOrm Marius[a]": "Ocean Master (Orm Marius)",
    "ScavengerPeter Mortimer": "Scavenger (Peter Mortimer)"
}

# Apply replacements
for villain in aquaman_villains:
    name = villain['villain']
    if name in replacements:
        villain['villain'] = replacements[name]

df = pd.DataFrame(aquaman_villains)
print(df)