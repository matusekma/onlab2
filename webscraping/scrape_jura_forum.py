import json, re

from parsing.get_soup import get_soup
from parsing.extract_qa import extract_qa_jura_forum
from utils import current_time_millisec


def scrape_topic_pages(topic):
    html_page_1 = get_soup(
            f'https://www.juraforum.de/ratgeber/{topic}/{1}')
    
    page_number_indicator = html_page_1.find(string=re.compile("Seite 1 von")) # returns ex. 'Seite 1 von 10:'
    page_number_string = page_number_indicator.strip().split(" ")[-1][:-1]
    page_number =  int(page_number_string) if len(page_number_string) > 0 else 1
    print(f'{page_number} pages in topic {topic}.')
    
    questions_and_answers = []
    for page in range(1, page_number + 1):
        print(f'Processing page: {page}')
        html = get_soup(
            f'https://www.juraforum.de/ratgeber/{topic}/{page}')

        articles = html.select("#spalte-inhalt .teaser-xl")
        for article in articles:
            article_url = article.h2.a["href"]
            article_html = get_soup(article_url)
            article_data = extract_qa_jura_forum(article_html)
            article_data["url"] = article_url
            questions_and_answers.append(article_data)

    return questions_and_answers


topics = ["arbeitsrecht", "bankrecht", "erbrecht", "familienrecht", "mietrecht",
          "mieterrechte", "strafrecht", "tierschutz", "urheberrecht", "urheberrecht", "verkehrsrecht", "corona"]

qa = []
for topic in topics:
    qa.extend(scrape_topic_pages(topic))
    print(len(qa))

json_string = json.dumps(qa)
json_string_pretty = json.dumps(qa, indent=4, separators=(",", ": "))

with open(f'./data/jura_forum_{current_time_millisec()}.json', 'w') as outfile:
    json.dump(json_string, outfile)
