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


def extract_qa_gutefrage(article):
    question = article.find("h1", class_="Question-title").get_text().strip()

    question_text = ""
    question_text_html = article.find("div", id="questiontext")
    if question_text_html is not None:
        question_text = question_text_html.get_text()

    # remove block qoutes
    for blockquote in article.findAll("blockquote"):
        blockquote.decompose()

    answer_cards_html = article.findAll("article", itemprop="suggestedAnswer")
    answers = []
    points = []
    for answer_card_html in answer_cards_html:
        answer_html = answer_card_html.find("div", class_="ContentBody")
        answers.append(clean_text(answer_html.get_text()))

        point_html = answer_card_html.find(
            "meta", itemprop="upvoteCount")
        if point_html is not None:
            points.append(point_html["content"])
        else:
            points.append("unk")

    return {"answers": answers, "points": points, "question": clean_text(question), "question_text": clean_text(question_text)}


def extract_qa_jusline(article):
    question = article.find("h2", class_="topic-title").get_text().strip()
    print(question)
    posts = article.findAll("div", class_="content")
    
    question_text = posts[0].get_text()

    answers = []
    for answer in posts[1:]:
        answers.append(clean_text(answer.get_text()))

    return {"answers": answers, "question": clean_text(question), "question_text": clean_text(question_text)}
