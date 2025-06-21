from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re
from crawler.portal_scraper import PortalScraper
import browser_cookie3
import ctypes
import sys
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit()

class CoursePKUScraper(PortalScraper):
    def fetch_assignments(self):

        if not is_admin():
            relaunch_as_admin()

        base_url = "https://course.pku.edu.cn"
        home_url = urljoin(base_url, "/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1")

        try:
            cj = browser_cookie3.chrome(domain_name='course.pku.edu.cn')
        except Exception as e:
            print("无法读取浏览器 cookie，请确保已登录 course.pku.edu.cn 并勾选“记住我”。")
            raise e
        cookies_dict = {cookie.name: cookie.value for cookie in cj}

        session = requests.Session()
        for name, value in cookies_dict.items():
            session.cookies.set(name, value)
        response = session.get(home_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        modules = soup.find_all("div", class_="portlet")
        course_urls = []
        for module in modules:
            title_tag = module.find("span", class_="moduleTitle")
            if title_tag and "当前学期课程" in title_tag.text:
                course_links = module.select("ul.courseListing.coursefakeclass a")
                for a_tag in course_links:
                    name = a_tag.get_text(strip=True)
                    launcher_url = urljoin(base_url, a_tag['href'])

                    res = session.get(launcher_url, allow_redirects=True)

                    final_url = res.url
                    course_urls.append((name, final_url))
        assignment_links = []
        for name, course_url in course_urls:
            res = session.get(course_url)
            soup = BeautifulSoup(res.text, 'html.parser')
            course_menu = soup.select("ul#courseMenuPalette_contents a")
            for a_tag in course_menu:
                span = a_tag.find("span")
                if span and "课程作业" in span.text:
                    hw_url = urljoin(base_url, a_tag['href'])
                    assignment_links.append((name, hw_url))
                    break
        import datetime

        year = datetime.datetime.now().year

        assignments = []

        for course_name, hw_url in assignment_links:
            res = session.get(hw_url)
            soup = BeautifulSoup(res.text, 'html.parser')

            items = soup.find_all('li', class_='liItem')
            for item in items:
                h3 = item.find('h3')
                if not h3:
                    continue
                a_tag = h3.find('a')
                if not a_tag:
                    continue
                title = a_tag.get_text(strip=True)

                info_divs = item.find_all('div', class_='vtbegenerated_div')
                combined_text = "\n".join(div.get_text(strip=True) for div in info_divs)
                date_match = re.search(r'(\d{1,2})月(\d{1,2})号', combined_text)
                if date_match:
                    month = int(date_match.group(1))
                    day = int(date_match.group(2))
                    try:
                        due_date = datetime.date(year, month, day)
                        due = due_date.isoformat()  # 格式为 yyyy-mm-dd
                    except ValueError:
                        due = "无效日期"
                else:
                    due = f"{year}-00-00"
                assignments.append((course_name[38:], title, due))
        print(assignments)
        return assignments
o = CoursePKUScraper()
print(o.fetch_assignments())
