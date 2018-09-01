from lxml import html
import json
import requests
import string
import sys
import urllib.request

# set config variables
with open("config.json") as cfg:
    config = json.load(cfg)

file_path = config["folder"]

while True:
    search = input("Enter search term: ")

    if search == "quit":
        break

    # search ff14angler
    search_result = requests.get("http://ff14angler.com/?search=" + search)
    
    # load the html
    tree = html.fromstring(search_result.content)

    # get the search results
    result = tree.xpath('//ul[@class="search_result"]//a/@href')
    name = tree.xpath('//ul[@class="search_result"]//a/text()')

    selection = 1
    if len(result) > 1:
        print("Multiple results found.")
        for x in range(len(result)):
            print (str(x+1) + ". " + string.capwords(name[x]))
        while True:
            try:     
                selection = int(input("Enter selection: "))
            except ValueError:
                pass
            else:
                break

    try: 
        # retrieve the selection's link
        link = "http://ff14angler.com" + tree.xpath('//ul[@class="search_result"]//a/@href')[selection-1]
    except IndexError:
        print("No results for " + search + " found.")
    else:    
        print(string.capwords(name[selection-1]) + "                     ", file=open(file_path + "\\target.txt", "w"))

        # load the selection's page
        page = requests.get(link)

        # load the html
        tree = html.fromstring(page.content)

        # consolidate image's link
        server_file = "http://ff14angler.com" + tree.xpath('//div[@class="clear_icon_l"]//img/@src')[0]

        # save the image
        urllib.request.urlretrieve(server_file, file_path + "\\target.png")