import requests
from bs4 import BeautifulSoup
from crawler.portal_scraper import PortalScraper

class OpenJudgeScraper(PortalScraper):
    def __init__(self):
        self.session = requests.Session()

    def fetch_assignments(self):
        url = "http://cxsjsx.openjudge.cn/"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        assignments = []
        titles = soup.find_all("li", attrs={"class": "contest-info"})
        if len(titles)>0:
            title = []
            for s in titles:
                all_title= s.find_all('h3')
                due = s.find_all('span', class_='over-time')
            for s in all_title:
                title.append(s.get_text(strip=True))
            for i in range(len(due)):
                assignments.append([
                    "程序设计实习",
                    title[i][1:],
                    due[i].string[5:15]
                ])
        url_1 = "http://dsalgo.openjudge.cn/"
        response_1 = self.session.get(url_1)
        soup_1 = BeautifulSoup(response_1.text, 'html.parser')
        titles_1 = soup_1.find_all("li", attrs={"class": "contest-info"})
        if len(titles_1)>0:
            title_1 = []
            for s in titles_1:
                all_title_1 = s.find_all('h3')
                due_1 = s.find_all('span', class_='over-time')
            for s in all_title_1:
                title_1.append(s.get_text(strip=True))
            for i in range(len(due_1)):
                assignments.append([
                   "数据结构分析",
                    title_1[i][1:],
                    due_1[i].string[5:15]
                ])
        return assignments
