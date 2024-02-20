import pickle

from bs4 import BeautifulSoup

from article_class import Article
from constants import DATA_FOLDER, SOURCES_FILE_NAME

articles_formatted = []
articles_formatted_no_duplicates = []

with open("../sources/en_jan_24_htmlversion.html") as fp:
    soup = BeautifulSoup(fp)


articles_raw = soup.find_all("div", class_="eli-subdivision")
for article in articles_raw:
    try:
        article_number = article.find("p", class_="title-article-norm").get_text()
        article_title = article.find("p", class_="stitle-article-norm").get_text()
        article_content = article.get_text()
        articles_formatted.append(Article(article_title=article_title,
                                          article_number=article_number,
                                          article_content=article_content))
        print(article_number)
    except AttributeError:
        print("Error with" + article.text)

for article in articles_formatted:
    shortest_article = article
    for article_check in articles_formatted:
        if article.article_number == article_check.article_number and len(article.article_content) > len(article_check.article_content):
            print("Removing " + article.article_number)
            shortest_article = None
    if shortest_article is not None:
        articles_formatted_no_duplicates.append(shortest_article)
save_path = f"../{DATA_FOLDER}{SOURCES_FILE_NAME}"
open_file = open(save_path, "wb")
pickle.dump(articles_formatted_no_duplicates, open_file)
open_file.close()


