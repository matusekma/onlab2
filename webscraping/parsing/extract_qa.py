import re


def clean_text(text):
    text_tokens = text.strip().replace('\n', ' ').replace(u'\xa0', u' ').split()
    # rejoin to remove multiple whitespaces
    return ' '.join(text_tokens)


def extract_qa_jura_fragen(article):
    question = article.find("h1", class_="entry-title").get_text()

    article_content = article.find("div", class_="entry-content")

    tags = []
    for tag in article_content.select("div.tag_list a"):
        tags.append(tag.get_text())

    tag_html = article_content.find("div", class_="tag_list")
    tag_html.decompose()

    answer = article_content.get_text()
    return {"answer": clean_text(answer), "tags": tags, "question": clean_text(question)}


def extract_qa_jura_forum(article):
    question = article.find("h1", itemprop="headline").get_text()

    tags = article.find(string=re.compile("Schlagwörter: "))
    if tags is not None:
        tags = tags.replace("Schlagwörter: ", "").split(" ")
        tags = [t.strip(",") for t in tags]
    else:
        tags = []

    answer = article.find("div", itemprop="articleBody").get_text()
    return {"answer": clean_text(answer), "tags": tags, "question": clean_text(question)}
