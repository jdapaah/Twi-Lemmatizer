import requests
import json
from bs4 import BeautifulSoup as bs
from os import mkdir, path

####################################################
#                                                  #
# Created by Ethan Haque (github.com/EthanHaque)   #
#                                                  #
# Adapted by Jeremy Dapaah (github.com/jdapaah)    #
#                                                  #
####################################################


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
root_url = "https://www.bible.com/"

def get_page(url):
    """Requests page of given url.

    Parameters
    ----------
    url : str
        URL to webpage.

    Returns
    -------
    str
        Webpage response string.
    """
    response = requests.get(url, headers={'User-Agent': user_agent})
    return response.text

def get_all_text_by_class_name(page_text, tag_type, class_name):
    """Gets text of all HTML elements with given class.

    Parameters
    ----------
    page_text : str
        HTML text data.
    tag_type : str
        Name of the HTML element.
    class_name : str
        Name of the class attribute of HTML element.

    Returns
    -------
    List
        List of strings of element content.
    """
    soup = bs(page_text, "html.parser")
    elements = soup.find_all(tag_type, class_name)
    return [element.text for element in elements]

def get_api_response(url):
    """Gets json response from api endpoint.

    Parameters
    ----------
    url : str
        URL to request.

    Returns
    -------
    Dict
        JSON-based dictionary from api response text.
    """
    response = requests.get(url, headers={'User-Agent': user_agent})
    api_response = json.loads(response.text)
    return api_response

def create_url_from_chapter_usfm(url, base_url, version):
    """Gathers informaiton about all chapters of book.

    Given url to api with response containing all chapter info,
    constructs urls to all the chapters in the book with given
    version extension. (ex. ASW).

    Parameters
    ----------
    url : str
        Url to api endpoint for chapter informaiton about a book.
    base_url : str
        Url used to construct chapters.
    version : str
        What version of bible to get.

    Returns
    -------
    List
        List of dicts that contain the name of the chapter and the usfm.
    """
    json_data = get_api_response(url)
    urls = []
    for item in json_data["items"]:
        url = base_url.format(item["usfm"] + "." + version)
        urls.append(url)
    return urls

# Getting all books and abbreviations.
books_url = root_url+"json/bible/books/1861"
books = get_api_response(books_url)

# Get the chapters in each book.
chapters_url = root_url+"json/bible/books/1861/{}/chapters"
all_chapters = {}

bible_url = root_url+"bible/1861/{}"
version = "ASW" # asante twi
for book in books["items"][-27:]: # collecte the new testament books
    book_name_abbreviation = book["usfm"]
    all_chapters[book_name_abbreviation] = create_url_from_chapter_usfm(
                                chapters_url.format(book_name_abbreviation),
                                bible_url,
                                version
                            )
rootPath = "./corpora/bible/"
if not path.exists(rootPath):   
    mkdir(rootPath)
for book_name, book in all_chapters.items():
    mkdir(rootPath+book_name)
    for i in range(1, len(book)):
        with open(rootPath+"{}/{}.txt".format(book_name, i), 'w') as file:
            html = get_page(book[i])
            text = get_all_text_by_class_name(html, "span", "content")
            file.write(' '.join(text))