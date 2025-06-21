import os
import requests
from dotenv import load_dotenv

class CanvasScraper:
    ENV_FILE = ".env"
    BASE_URL_DEFAULT = "https://canvas.pku.edu.cn"

    def __init__(self):
        self.token = None
        self.base_url = None
        self._load_or_create_env()

    def _create_env_file(self):
        print("检测到当前目录无 .env 文件，开始创建...")
        token = input("请输入你的 Canvas API Token（访问令牌）：").strip()
        if not token:
            print("Token 不能为空，请重新运行程序。")
            exit(1)

        with open(self.ENV_FILE, "w", encoding="utf-8") as f:
            f.write(f"CANVAS_BASE_URL={self.BASE_URL_DEFAULT}\n")
            f.write(f"CANVAS_API_TOKEN={token}\n")

        print(".env 文件已创建并保存了你的 Token。")

    def _load_or_create_env(self):
        if not os.path.exists(self.ENV_FILE):
            self._create_env_file()

        load_dotenv(self.ENV_FILE)
        self.token = os.getenv("CANVAS_API_TOKEN")
        self.base_url = os.getenv("CANVAS_BASE_URL") or self.BASE_URL_DEFAULT

        if not self.token:
            print(".env 文件中没有找到 CANVAS_API_TOKEN，请检查。")
            exit(1)

    def fetch_assignments(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        assignments = []

        # 获取当前用户所有活跃课程
        courses_url = f"{self.base_url.rstrip('/')}/api/v1/courses"
        params = {"enrollment_state": "active", "per_page": 100}
        response = requests.get(courses_url, headers=headers, params=params,verify = False)
        if response.status_code != 200:
            raise Exception(f"获取课程失败，状态码: {response.status_code}")

        courses = response.json()

        for course in courses:
            course_id = course.get("id")
            course_name = course.get("name")

            # 获取该课程的所有作业
            assignments_url = f"{self.base_url.rstrip('/')}/api/v1/courses/{course_id}/assignments"
            r = requests.get(assignments_url, headers=headers, params={"per_page": 100})
            if r.status_code != 200:
                print(f"无法获取课程 {course_name} 的作业，状态码 {r.status_code}")
                continue

            assignments_data = r.json()
            for a in assignments_data:
                title = a.get("name") or "（无标题）"
                due_at = a.get("due_at") or ""
                due_str = due_at[:10] if due_at else "无"
                assignments.append({
                    "course": course_name,
                    "title": title,
                    "due_date": due_str,
                })

        return assignments
'''
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("CANVAS_API_TOKEN")
    
    scraper = CanvasScraper()
    try:
        assignments = scraper.fetch_assignments()
        for a in assignments:
            print(f"{a['course']} | {a['title']} | {a['due_date']}")
    except Exception as e:
            print("错误:", e)
'''
