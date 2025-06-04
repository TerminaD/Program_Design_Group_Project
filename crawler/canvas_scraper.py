import requests
from crawler.portal_scraper import PortalScraper

class CanvasScraper(PortalScraper):
    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url.rstrip("/")

    def fetch_assignments(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/api/v1/users/self/todo", headers=headers)
        if response.status_code != 200:
            raise Exception("Canvas API 请求失败")

        data = response.json()
        assignments = []
        for item in data:
            assignment = item.get("assignment", {})
            assignments.append({
                "title": assignment.get("name"),
                "description": assignment.get("description", ""),
                "due_date": assignment.get("due_at"),
            })
        return assignments
