import requests
import xml.etree.ElementTree as ET
import datetime
from todo.models import Article


def get_articles_with_details():
    all_articles = []
    abs_tree = get_article_list_xml()

    for title in abs_tree.findall('PubmedArticle/MedlineCitation'):
        article_id = get_article_id(title)
        article_title = get_article_title(title)
        article_abstract = get_article_abstract(title)
        author_list = get_article_author_list(title)
        keyword_list = get_article_keyword_list(title)
        pub_date = get_article_pub_date(title)

        # articles = models.Article(
        #     article_id=article_id,
        #     article_title=article_title,
        #     article_abstract=article_abstract,
        #     author_list=author_list,
        #     keyword_list=keyword_list,
        #     pub_date=pub_date
        # )

        try:
            article = Article.objects.get(article_id=article_id)
            article.article_title = article_title
            article.article_abstract = article_abstract
        except Article.DoesNotExist:
            article = Article.objects.create(
                article_id=article_id,
                article_title=article_title,
                article_abstract=article_abstract,
                author_list=author_list,
                keyword_list=keyword_list,
                pub_date=pub_date
            )


        # print(articles)

        # each_article_row = [
        #     article_id,
        #     article_title,
        #     article_abstract,
        #     author_list,
        #     pub_date,
        #     keyword_list,
        # ]
        #
        # print(each_article_row)

        article.save()

        all_articles.append(article)

    return all_articles


def get_article_list_xml():
    article_ids = get_article_ids()
    article_ids_as_string = ','.join(article_ids)
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=" + article_ids_as_string + "&rettype=abstract"
    # print(url)
    response = requests.request("POST", url)
    # print(response)
    article_xml_tree = ET.fromstring(response.content)

    return article_xml_tree


def get_article_ids():
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=aids+AND&retmode=json&retmax=5"

    response = requests.request("GET", url)
    articles = response.json()

    article_list = []
    for i in range(len(articles['esearchresult']['idlist'])):
        article_list.append(articles['esearchresult']['idlist'][i])

    # print(article_list)
    return article_list


def get_article_pub_date(title):
    pubdate = ""

    try:
        for date in title.findall('Article/Journal/JournalIssue/PubDate'):
            year = str(date.find('Year').text)
            month = str(datetime.datetime.strptime(str(date.find('Month').text), '%b').month)
            day = str(date.find("Day").text)
            pubdate = year + "/" + month + "/" + day + " 00:00"
            pubdate = datetime.datetime.strptime(pubdate, '%Y/%m/%d %H:%M')
    except:
        print("Couldn't get the publish date")
        pass

    return pubdate


def get_article_keyword_list(title):
    keyword_list = ""

    try:
        for keyword in title.findall('KeywordList/Keyword'):
            keyword_list += str(keyword.text) + ";"
        keyword_list = keyword_list.strip(";")
        # print(keyword_list)
    except:
        print("Couldn't get the keyword")
        pass

    return keyword_list


def get_article_author_list(title):
    author_list = ""

    try:
        for author in title.findall('Article/AuthorList/Author'):
            author_name = author.find('LastName').text + " " + author.find('ForeName').text + ";"
            author_list += author_name
        author_list = author_list.strip(';')
        # print(author_list)
    except:
        print("Couldn't get the author")
        pass

    return author_list


def get_article_abstract(title):
    abstract_all = ""

    for abstract in title.findall('Article/Abstract/AbstractText'):
        abstract_all += str(abstract.text)

    return abstract_all


def get_article_title(title):
    article_title = title.find('Article/ArticleTitle').text

    return article_title


def get_article_id(title):
    article_id = title.find('PMID').text

    return article_id
