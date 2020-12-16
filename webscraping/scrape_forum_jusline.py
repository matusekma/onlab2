import json
import re

from parsing.get_soup import get_soup
from parsing.extract_qa import extract_qa_jusline
from utils import current_time_millisec


def scrape_topic(topic_url):
    questions_and_answers = []

    html_page = get_soup(f'https://forum.jusline.at/{topic_url}')
    topic_title = html_page.find("h2", class_="forum-title").get_text()
    print(topic_title)

    page = 1
    while True:
        print(f'PROCESSING PAGE: {page}')

        rows = html_page.findAll("dl", class_="row-item topic_read")

        for row in rows:
            try:
                answer_num = row.find("dd", class_="posts")
                if answer_num is None or answer_num.get_text() == "0 Antworten":
                    continue
                article_url = row.find("a", class_="topictitle")["href"][1:]
                article_url = f'https://forum.jusline.at/{article_url}'
                article_html = get_soup(article_url)
                article_data = extract_qa_jusline(article_html)
                article_data["url"] = article_url
                article_data["topic"] = topic_title
                questions_and_answers.append(article_data)
            except BaseException as e:
                print("ERROR PROCESSING ARTICLE")
                print(e)
            # print(article_data)

        next_page_button_link = html_page.find(
            "a", class_="button", rel="next")
        if next_page_button_link is None:
            break

        next_page_url = next_page_button_link["href"]
        html_page = get_soup(f'https://forum.jusline.at/{next_page_url}')
        page += 1

    return questions_and_answers


def scrape_topic_pages():
    html_page_starter = get_soup('https://forum.jusline.at/')

    forum_topic_urls = html_page_starter.findAll("a", class_="forumtitle")

    # get href and remove . from relative path
    forum_topic_urls = [link["href"][1:] for link in forum_topic_urls]

    forum_topic_urls = forum_topic_urls[:-1]

    questions_and_answers = []
    for topic_url in forum_topic_urls:
        questions_and_answers.extend(scrape_topic(topic_url))
        with open(f'./data/forum_jusline_checkpoint.json', 'w') as outfile:
            json.dump(questions_and_answers, outfile)

    return questions_and_answers


qa = scrape_topic_pages()
# qa = []
# for topic in topics:
#     qa.extend(scrape_topic_pages(topic))
print(len(qa))

# json_string_pretty = json.dumps(qa, indent=4, separators=(",", ": "))

with open(f'./data/forum_jusline_{current_time_millisec()}.json', 'w') as outfile:
    json.dump(qa, outfile)
