import requests
from bs4 import BeautifulSoup
from .portal_scraper import PortalScraper

class CoursePKUScraper(PortalScraper):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        login_url = "https://course.pku.edu.cn/webapps/login/"
        payload = {
            "user_id": self.username,
            "password": self.password
        }
        # 模拟表单登录
        response = self.session.post(login_url, data=payload)
        if response.status_code != 200 or "登录失败" in response.text:
            raise Exception("教学网登录失败")

    def fetch_assignments(self):
        self.login()
        homework_url = "https://course.pku.edu.cn/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1"
        response = self.session.get(homework_url)
        soup = BeautifulSoup(response.text, "html.parser")

        assignments = []
        for item in soup.select(".assignmentRow"):
            title = item.select_one(".assignmentTitle").text.strip()
            due = item.select_one(".assignmentDue").text.strip()
            description = item.select_one(".assignmentDescription").text.strip() if item.select_one(".assignmentDescription") else ""
            assignments.append({
                "title": title,
                "description": description,
                "due_date": due
            })
        return assignments
