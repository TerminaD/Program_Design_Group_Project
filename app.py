import sqlite3
import tkinter as tk
from data.database import DatabaseManager
from crawler.portal_scraper import PortalScraper
from backend.controller import Controller
from gui.main_window import MainWindow


def main():
    # Initialize SQLite connection and database
    conn = sqlite3.connect("app.db")
    db = DatabaseManager(conn)
    db.initialize()

    # Initialize crawler and controller
    crawler = PortalScraper()
    controller = Controller(db, crawler)

    # Start GUI
    root = tk.Tk()
    root.title("Homework & Exams")
    app = MainWindow(root, controller)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
