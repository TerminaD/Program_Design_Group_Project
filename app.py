import sqlite3
import tkinter as tk
from data.database import DatabaseManager
from crawler.canvas_scraper import CanvasScraper
from crawler.course_scraper import CoursePKUScraper
from crawler.openjudge_scraper import OpenJudgeScraper
from backend.controller import Controller
from gui.main_window import MainWindow


def main():
    # Initialize SQLite connection and database
    conn = sqlite3.connect("app.db")
    db = DatabaseManager(conn)
    db.initialize()

    # Initialize crawler and controller
    canvas_scraper = CanvasScraper()
    course_scraper = CoursePKUScraper()
    openjudge_scraper = OpenJudgeScraper()
    controller = Controller(db, canvas_scraper, course_scraper, openjudge_scraper)

    # Start GUI
    root = tk.Tk()
    root.title("Homework & Exams")
    app = MainWindow(root, controller)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
