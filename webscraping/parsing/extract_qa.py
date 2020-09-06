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
