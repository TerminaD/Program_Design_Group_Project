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

    if not is_admin():
        relaunch_as_admin()
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
    is_debug = False

    # Initialize SQLite connection and database
    conn = sqlite3.connect("app.db")
    db = DatabaseManager(conn)
    db.initialize()

    app = tk.Tk()

    # Initialize crawler and controller
    if is_debug:
        controller = DebugController(db)
    else:
        canvas_scraper = CanvasScraper(root_for_dialog=app)
        course_scraper = CoursePKUScraper()
        openjudge_scraper = OpenJudgeScraper()
        controller = Controller(db, canvas_scraper, course_scraper, openjudge_scraper)

    app.geometry("1920x1080")
    app.title("Group Project")
    app["bg"] = "white"
    create_main_interface(app, controller)
    app.mainloop()


if __name__ == "__main__":
    main()
