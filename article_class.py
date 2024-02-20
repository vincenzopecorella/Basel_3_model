class Article:
    article_number = None
    article_title = None
    article_content = None

    def __init__(self, article_number, article_title, article_content):
        self.article_number = article_number
        self.article_content = article_content
        self.article_title = article_title
