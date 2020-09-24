import json
import re

from parsing.get_soup import get_soup
from parsing.extract_qa import extract_qa_gutefrage
from utils import current_time_millisec


def scrape_pages():
    page = 1
    questions_and_answers = []
    while True:

        print(f'Processing page: {page}')
        html = get_soup(
            f'https://www.gutefrage.net/tag/recht/{page}')

        # check if error page was reached
        error_page_section = html.select("section.ErrorPageSection")
        if len(error_page_section) != 0:
            break

        article_cards = html.select(
            "article.ListingElement.Plate a.ListingElement-questionLink")
        for article_card in article_cards:
            try:
                article_url = f'https://www.gutefrage.net{article_card["href"]}'
                print(article_url)
                article_html = get_soup(article_url)
                article_data = extract_qa_gutefrage(article_html)
                article_data["url"] = article_url
                questions_and_answers.append(article_data)
            except BaseException as e:
                print("ERROR PROCESSING ARTICLE")
                print(e)

        # checkpoint
        if page % 2 == 0:
            print(len(questions_and_answers))
            json_string = json.dumps(questions_and_answers)
            with open(f'./data/gute_frage.json', 'w') as outfile:
                json.dump(json_string, outfile)

        page += 1

    return questions_and_answers


qa = scrape_pages()

json_string = json.dumps(qa)
json_string_pretty = json.dumps(qa, indent=4, separators=(",", ": "))

with open(f'./data/gute_frage_{current_time_millisec()}.json', 'w') as outfile:
    json.dump(json_string, outfile)
with open(f'./data/gute_frage_pretty_{current_time_millisec()}.json', 'w') as outfile:
    json.dump(json_string_pretty, outfile)
