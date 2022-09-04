import sys
from collections import Counter

import bs4
import mdprint as md
import requests


def parse_table(soup):
    table_rows = soup.table.tbody.find_all("tr")[1:]

    countries_gen = (tr.find_all("td")[3].get_text() for tr in table_rows)
    countries = [country for country in countries_gen if country != ""]

    total = len(countries)
    countries_counter = Counter(countries)
    germans_num = countries_counter["Германия"] + countries_counter["Австрия"] + countries_counter["ФРГ"]
    germans_percent = round(germans_num / total, 2)
    countries_counter_table = countries_counter.most_common()

    return countries_counter_table, total, germans_percent


def main(output=sys.stdout):
    pages = {
        "Премия мира": "https://megabook.ru/article/Список%20лауреатов%20нобелевских%20премий%20мира%20по%20годам",
        "Премия по литературе": "https://megabook.ru/article/Список%20лауреатов%20нобелевских%20премий%20по%20литературе%20по%20годам",
        "Премия по физике": "https://megabook.ru/article/Список%20лауреатов%20нобелевских%20премий%20по%20физике%20по%20годам",
        "Премия по физиологии и медицине": "https://megabook.ru/article/Список%20лауреатов%20нобелевских%20премий%20по%20физиологии%20и%20медицине%20по%20годам",
        "Премия по химии": "https://megabook.ru/article/Список%20лауреатов%20нобелевских%20премий%20по%20химии%20по%20годам",
        "Премия по экономике": "https://megabook.ru/article/Список%20лауреатов%20нобелевских%20премий%20по%20экономике%20по%20годам",
    }

    md.mdprint("Количество нобелевских лауреатов по странам\n", heading=1, file=output)

    for title, url in pages.items():
        response = requests.get(url)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "html5lib")

        countries_counter_table, total, germans_percent = parse_table(soup)
        md.mdprint(title, heading=2, file=output)
        
        table_list = [('Страна', 'Число лауреатов')]
        table_list.extend(countries_counter_table)
        table_list.append(('ВСЕГО', total))

        md.mdprint_list(table_list, file=output)

        md.mdprint(
            f"Процент лауреатов из Германии и Австрии: {germans_percent:.2f}",
            bold=True,
            file=output,
        )
        print(file=output)


if __name__ == "__main__":
    with open("README.md", "w") as output:
        main(output)
