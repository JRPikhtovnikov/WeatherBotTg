import newspaper
import random
from newspaper import Article
# url = 'https://proglib.io/p/9-luchshih-praktik-po-rabote-s-mikroservisami-2023-04-09'
# article = Article(url)
# article.download()
# article.parse()
#
# print(article.title)
# print(article.text)


paper = newspaper.build('https://proglib.io/', memoize_articles=False)


article = paper.articles[0]
print(article.url)
