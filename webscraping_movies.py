import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies.db'
table_name = 'Top_25_2000s'
csv_path = 'top_25_films_2000s.csv'

# Create DataFrame with required columns
df = pd.DataFrame(columns=["Film", "Year", "Rotten Tomatoes' Top 100"])

html_page = requests.get(url).text
soup = BeautifulSoup(html_page, 'html.parser')

tables = soup.find_all('tbody')
rows = tables[0].find_all('tr')

count = 0

for row in rows:
    if count < 25:
        cols = row.find_all('td')
        if len(cols) != 0:
            year = int(cols[2].text.strip())

            # Filter films released in 2000s (2000 included)
            if year >= 2000:
                data_dict = {
                    "Film": cols[1].text.strip(),
                    "Year": year,
                    "Rotten Tomatoes' Top 100": cols[3].text.strip()
                }

                df = pd.concat([df, pd.DataFrame(data_dict, index=[0])],
                               ignore_index=True)
                count += 1
    else:
        break

# Print filtered output
print(df)

# Save to CSV
df.to_csv(csv_path, index=False)

# Save to SQLite
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()
