import requests
import re
import time
from bs4 import BeautifulSoup
import xlwt


class Crawler:

    def __init__(self, seed_url, max_depth=5, max_links=1000, keywords=""):
        self.wait = 1
        self.max_depth = max_depth
        self.total_links = max_links
        self.seed_url = seed_url
        self.res = [seed_url]
        self.keywords = keywords
        # self.count = 0
        self.header = "https://en.wikipedia.org"
        self.linklistRes = set()

    def links_in_page(self, url):

        time.sleep(self.wait)
        bs = BeautifulSoup(self.get_html(url), 'lxml')
        # self.count += 1
        link_list = []

        for link in bs.find_all('a'):

            # Restriction of 1000 links
            if len(self.linklistRes) >= self.total_links:
                break

            relative_link = link.get('href')
            if type(relative_link) is str:
                exp = re.match("^/wiki/*.*", relative_link)
                if exp is not None and ":" not in exp.group() and "Main_Page" not in exp.group():

                    # keywords check
                    if self.keywords is not None and self.keyWordsCheck(exp.group(), self.keywords) is False:
                        continue
                    # if self.keywords is not None and self.keywords not in exp.group():
                    #     continue

                    if exp.group() not in self.linklistRes:
                        link_list.append(exp.group())

                    self.linklistRes.add(exp.group())

        print("Number of links:", len(self.linklistRes), end=" ")

        # for deeper pages
        # header = "https://en.wikipedia.org"
        link_list_new = []

        for link in link_list:
            # print(link)
            link_list_new.append(self.header + link)

        # self.Out2File(link_list_new)

        return link_list_new

    def searchPages(self):
        # In a BFS way
        pages = 1
        depth = {}
        depth[self.seed_url] = 1
        queue = []
        queue.append(self.seed_url)
        for url in queue:

            # Restrictions of 5 maximum depth
            if depth[url] > self.max_depth:
                print("Maximum depth reached:", self.max_depth)
                print("Total links: ", len(self.linklistRes))
                break

            link_list = self.links_in_page(url)
            # print(depth.values())

            pages += 1
            print("From depth:", depth[url])
            for link in link_list:
                if link not in depth:
                    # print(depth)
                    depth[link] = depth[url] + 1
                    # self.res.append(link)
                    queue.append(link)
                    if len(self.linklistRes) >= self.total_links:
                        print("Maximum links reached")
                        print("Current depth: ", depth[url])
                        self.Out2File(self.linklistRes)
                        return

        self.Out2File(self.linklistRes)
        return

    def Out2File(self, link_list):
        # with open("hwk1" + str(self.count) + ".txt", mode="w+", encoding="utf-8") as f:
        #     for link in link_list:
        #         f.write(link + "\n")
        header = "https://en.wikipedia.org"
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)

        for i in range(0, len(link_list)):
            booksheet.write(i, 0, self.header + link_list.pop())
        if self.keywords is None:
            workbook.save('hwk1WithoutKeyWords.xls')
            print("File hwk1WithoutKeyWords.xls saved")
        else:
            workbook.save('hwk1WithKeyWords.xls')
            print("File hwk1WithKeyWords.xls saved")
        # print("links stored in txt file!", " Name: hwk1" + str(self.count) + ".txt")

    def test(self):
        self.links_in_page(self.seed_url)

    def keyWordsCheck(self, url, keywords):
        header = "https://en.wikipedia.org"
        url = self.header + url
        bs = BeautifulSoup(self.get_html(url), 'lxml')
        # print(bs.find('p'))
        # print("======================")
        text = bs.find('p').text.strip()
        if len(text) == 0:
            return False

        if keywords in text:
            return True
        else:
            return False

    def get_html(self, url):
        # try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
        # except:
        #     return"error! failed to get html"

base_url = 'https://en.wikipedia.org/wiki/Karen_Sparck_Jones'


obj1 = Crawler(seed_url=base_url, keywords="retrieval")

obj2 = Crawler(seed_url=base_url, keywords=None)

# Crawler.test(obj)

start = time.time()
Crawler.searchPages(obj1)
end = time.time()
print("Time: ", end - start)

start = time.time()
Crawler.searchPages(obj2)
end = time.time()
print("Time: ", end - start)
