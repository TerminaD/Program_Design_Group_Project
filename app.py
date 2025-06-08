import sqlite3
import tkinter as tk

from data.database import DatabaseManager
from crawler.canvas_scraper import CanvasScraper
from crawler.course_scraper import CoursePKUScraper
from crawler.openjudge_scraper import OpenJudgeScraper
from backend.controller import Controller, DebugController
from gui.main_interface import create_main_interface


def main():
    # 在 debug 模式下，不进行爬虫，使用一个占位数据库
    is_debug = True

    # Initialize SQLite connection and database
    conn = sqlite3.connect("app.db")
    db = DatabaseManager(conn)
    db.initialize()

    # Initialize crawler and controller
    if is_debug:
        controller = DebugController(db)
    else:
        canvas_scraper = CanvasScraper()
        course_scraper = CoursePKUScraper()
        openjudge_scraper = OpenJudgeScraper()
        controller = Controller(db, canvas_scraper, course_scraper, openjudge_scraper)

    app = tk.Tk()
    app.geometry("1920x1080")
    app.title("Group Project")
    app["bg"] = "white"
    create_main_interface(app, controller)
    app.mainloop()


if __name__ == "__main__":
    main()
