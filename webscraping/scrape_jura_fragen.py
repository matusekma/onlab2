import json

from parsing.get_soup import get_soup
from parsing.extract_qa import extract_qa_jura_fragen
from utils import current_time_millisec


def scrape_topic_pages(topic):
    page = 1
    questions_and_answers = []
    while True:
        print(f'Processing page: {page}')
        html = get_soup(
            f'https://jura-fragen.de/rechtsgebiet/{topic}/page/{page}')
        if 'error404' in html.body["class"]:    # no more pages
            break

        articles = html.find_all(class_="entry-title")
        for article_title in articles:
            article_url = article_title.a["href"]
            article_html = get_soup(article_url)
            article_data = extract_qa_jura_fragen(article_html)
            article_data["url"] = article_url
            questions_and_answers.append(article_data)
        page += 1

    return questions_and_answers


topics = ["zivilrecht", "oeffentliches-recht", "strafrecht"]

qa = []
for topic in topics:
    qa.extend(scrape_topic_pages(topic))
    print(len(qa))

json_string = json.dumps(qa)
json_string_pretty = json.dumps(qa, indent=4, separators=(",", ": "))

with open(f'./data/jura_fragen_{current_time_millisec()}.json', 'w') as outfile:
    json.dump(json_string, outfile)

print(json_string_pretty)
