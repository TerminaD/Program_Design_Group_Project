import tkinter as tk
from tkinter import ttk


class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # UI elements
        self.tree = ttk.Treeview(self, columns=("Due",), show="headings")
        self.tree.heading("Due", text="Due Date")
        self.tree.pack(fill="both", expand=True)

        self.refresh_btn = ttk.Button(self, text="Refresh", command=self.on_refresh)
        self.refresh_btn.pack(pady=5)

        # Initial load
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for subject, content, due_date in self.controller.load_assignments():
            self.tree.insert("", "end", values=(subject, content, due_date))

    def on_refresh(self):
        items = self.controller.refresh_assignments()
        # Update view
        self.load_data()
