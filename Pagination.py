from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

item = "redmi note 9 pro"
item = item.replace(" ", "")
flip_url = "https://flipkart.com/search?q=" + item      # preparing the URL
uSearch = urlopen(flip_url)     # requesting page
flipPage = uSearch.read()   # reading the webpage
uSearch.close()     # closing connection

# parsing product list page
flip_html = bs(flipPage, "html.parser")     # parsing the html
boxes = flip_html.find_all("div", attrs={'class': '_2pi5LC col-12-12'})      # finding all div
del boxes[0:3]
box = boxes[0]
productLink = "https://flipkart.com" + box.div.div.div.a['href']    # getting product link
productPage = requests.get(productLink)     # opening the product link
prod_html = bs(productPage.text, "html.parser")     # parsing the html
rating_link = prod_html.find("div", attrs={"class": 'col JOpGWq'})     # getting all reviews link
# print(rating_link)
for i in range(1, 101):
    all_rating_link = "https://flipkart.com" + rating_link.find_all("a")[-1]["href"] + "&page=" + str(i)
    # parsing all reviews page
    all_rating_Page = requests.get(all_rating_link)
    rating_html = bs(all_rating_Page.text, "html.parser")
    comments = rating_html.find_all("div", attrs={'class': '_27M-vq'})

    # retrieving comments
    for comment in comments:
        try:
            name = comment.div.div.find_all('p', attrs={'class': '_2sc7ZR _2V5EHH'})[0].text
        except:
            name = 'No name'

        try:
            rating = comment.div.div.div.div.text
        except:
            rating = 'No rating'

        try:
            cmntHead = comment.div.div.div.p.text
        except:
            cmntHead = 'No comment head'

        try:
            review = comment.div.div.find_all('div', attrs={'class': ''})[0].text
        except:
            review = 'Nothing'

        data = {'Customer Name': name, 'Rating': rating, 'Comment Head': cmntHead, 'Review': review}
        print(data)