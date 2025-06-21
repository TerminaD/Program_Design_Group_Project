from data.database import DatabaseManager
from crawler.canvas_scraper import CanvasScraper
from crawler.course_scraper import CoursePKUScraper
from crawler.openjudge_scraper import OpenJudgeScraper


class Controller:
    def __init__(
        self,
        db: DatabaseManager,
        canvas_scraper: CanvasScraper,
        course_scraper: CoursePKUScraper,
        openjudge_scraper: OpenJudgeScraper,
    ):
        self.db = db
        self.canvas_scraper = canvas_scraper
        self.course_scraper = course_scraper
        self.openjudge_scraper = openjudge_scraper
        self.refresh_assignments()

    def load_assignments(self):
        return self.db.get_assignments()

    def load_exams(self):
        return self.db.get_exams()

    def refresh_assignments(self):
        canvas_items = self.canvas_scraper.fetch_assignments()
        course_items = self.course_scraper.fetch_assignments()
        openjudge_items = self.openjudge_scraper.fetch_assignments()
        items = canvas_items + course_items + openjudge_items
        self.db.delete_all_scraper_assignments()
        for item in items:
            self.db.add_assignment(
                item["title"], item["description"], item["due_date"], "scraper"
            )
        return items

    def user_add_assignment(self, subject: str, content: str, due_date: str):
        self.db.add_assignment(subject, content, due_date, "user")

    def user_add_exam(self, subject: str, due_date: str):
        self.db.add_exam(subject, due_date)

    def delete_assignment(self, id: int):
        self.db.delete_assignment(id)

    def delete_exam(self, id: int):
        self.db.delete_exam(id)


class DebugController(Controller):
    def __init__(self, db: DatabaseManager):
        super().__init__(db, None, None, None)
        self.placeholders = [
            {"title": "CONTROLLER", "description": "Complete exercises 5 to 10 on page 123.", "due_date": "2025-05-29"},
            {"title": "Physics", "description": "Prepare lab report on thermodynamics.", "due_date": "2025-05-28"},
            {"title": "History", "description": "Write a 1000-word essay about World War II.", "due_date": "2025-06-01"},
            {"title": "English", "description": "Read chapters 4 and 5 and answer the questions.", "due_date": "2025-05-30"},
        ]
        self.db.delete_all_tables()
        self.db.initialize()
        for item in self.placeholders:
            self.db.add_assignment(
                item["title"], item["description"], item["due_date"], "scraper"
            )
