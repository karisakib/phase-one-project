from app import db, Database
from bs4 import BeautifulSoup 
import requests

r = requests.get("https://en.wikipedia.org/wiki/Top_contributors_to_greenhouse_gas_emissions")
soup = BeautifulSoup(r.text, features="html.parser")
table = soup.find('table')
rows = table.find_all("tr")

clean_data = []
for row in rows[1:]:
    link = row.find('a')["href"]
    stripped_list = list(row.stripped_strings)
    stripped_list.append(f"https://en.wikipedia.org{link}")
    clean_data.append(stripped_list)

def main():
    db.drop_all()
    db.create_all()

    for row in clean_data:
        new_row = Database(rank=row[0], company=row[1], country=row[2], percentage=row[3], link=row[4])
        db.session.add(new_row)
        db.session.commit()

if __name__ == "__main__":
    main()