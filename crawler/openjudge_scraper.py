import requests
from bs4 import BeautifulSoup
from .portal_scraper import PortalScraper

class OpenJudgeScraper(PortalScraper):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        login_url = "http://openjudge.cn/account/login/"
        payload = {
            "username": self.username,
            "password": self.password
        }

        response = self.session.post(login_url, data=payload)
        if response.status_code != 200:
            raise Exception("OpenJudge 登录请求失败")

        # 判断是否登录成功（比如检查是否跳转到用户主页，或者页面中包含“退出”链接）
        if "logout" not in response.text.lower():
            raise Exception("OpenJudge 登录失败，请检查用户名密码")

    def fetch_assignments(self):
        self.login()
        url = "http://openjudge.cn/homework"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        assignments = []

        for row in soup.select(".homework-row"):
            title = row.select_one(".title").text.strip()
            due = row.select_one(".due-date").text.strip()
            assignments.append({
                "title": title,
                "description": "",
                "due_date": due
            })
        return assignments
