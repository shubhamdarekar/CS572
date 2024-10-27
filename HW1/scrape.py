from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
import json

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep: # Prevents loading too many pages too soon
            sleeptime = randint(10, 30)
            print("Sleeping:",sleeptime)
            time.sleep(sleeptime)
        temp_url = '+'.join(query.split()) #for adding + between words for the query

        url = 'http://www.bing.com/search?q=' + temp_url +"&count=25"
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results
    
    @staticmethod
    def scrape_search_result(soup):

        raw_results = soup.find_all("li", attrs = {"class" : "b_algo"})
        results = []
        total=0

        for result in raw_results:
            link = result.find_all("a")[0].get('href')
            if link is None or link in results or total >=10 or "http" not in link:
                continue
            results.append(link)
            total += 1
        # print(link)
        return results
    
    @staticmethod
    def read_queries():
        queries = []
        with open('100QueriesSet1.txt','r') as f:
            for line in f:
                queries.append(line.strip())
        return queries

#############Driver code############

queries = SearchEngine.read_queries()
bing_result_set = {}

for query in queries:
    result_set = SearchEngine.search(query,False)
    bing_result_set[query] = result_set

with open("Bing_Result1.json","w") as f:
    json.dump(bing_result_set,f,indent=4)
# print(bing_result_set)
####################################

