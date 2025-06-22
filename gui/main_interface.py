import tkinter as tk
from datetime import datetime

from .interface import (
    create_rounded_block,
    open_web_window,
    HomeworkList,
    FinalExamList,
    add_homework,
    get_final_exam_y
)


def create_main_interface(app1, controller):
    # --- Scrollable Canvas Setup ---
    canvas = tk.Canvas(app1, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(app1, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Enable mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # --- All content below goes into scrollable_frame instead of app1 ---
    label = tk.Label(
        scrollable_frame,
        text="选择教学平台",
        font=("Helvetica", 38, "bold"),
        fg="black",
        bg="white",
        padx=20,
        pady=30,
    )
    label.pack()

    # --- Platform blocks in a horizontal frame ---
    block_frame = tk.Frame(scrollable_frame, bg="white")
    block_frame.pack(pady=10)
    block_width = 150
    spacing = 40  # Use a fixed spacing for pack layout
    
    create_rounded_block(
        block_frame,
        x=0, y=0,  # x/y ignored in pack layout
        color="#e3ebfc",
        image_path="assets/pku.png",
        open_window=lambda: open_web_window("https://Pku.instructure.com"),
        text="PKU Canvas",
    ).pack(side="left", padx=spacing)
    create_rounded_block(
        block_frame,
        x=0, y=0,
        color="#e3ebfc",
        image_path="assets/poj.png",
        open_window=lambda: open_web_window("http://cxsjsx.openjudge.cn"),
        text="OpenJudge",
    ).pack(side="left", padx=spacing)
    create_rounded_block(
        block_frame,
        x=0, y=0,
        color="#e3ebfc",
        image_path="assets/jxw.png",
        open_window=lambda: open_web_window("https://course.pku.edu.cn"),
        text="北京大学教学网",
    ).pack(side="left", padx=spacing)

    # --- Homework and input section in a horizontal frame ---
    content_frame = tk.Frame(scrollable_frame, bg="white")
    content_frame.pack(pady=30, fill="x", expand=True)

    raw_homework_data = controller.load_assignments()
    homework_data = [
        {
            "subject": item[0],
            "description": item[1],
            "deadline": datetime.strptime(item[2], "%Y-%m-%d") if item[2] != "无" else None,
        }
        for item in raw_homework_data
    ]
    
    raw_final_exam_data = controller.load_exams()
    final_exam_data = [
        {"subject": item[0], "exam_date": datetime.strptime(item[1], "%Y-%m-%d")}
        for item in raw_final_exam_data
    ]

    # Homework list
    hw_list = HomeworkList(content_frame, homework_data)
    hw_list.pack(side="left", padx=30, anchor="n")

    # Input section
    input_frame = tk.Frame(
        content_frame, bg="#e3ebfc", highlightbackground="#4a7abc", highlightthickness=2
    )
    input_frame.pack(side="left", padx=30, anchor="n")
    # Labels and entries
    tk.Label(
        input_frame, text="科目:", font=hw_list.cell_font, bg="#e3ebfc", fg="black"
    ).grid(row=0, column=0, sticky="w", padx=8, pady=4)
    subject_entry = tk.Entry(
        input_frame, font=hw_list.cell_font, width=30, bg="white", fg="black"
    )
    subject_entry.grid(row=1, column=0, padx=8, pady=4)

    tk.Label(
        input_frame, text="描述:", font=hw_list.cell_font, bg="#e3ebfc", fg="black"
    ).grid(row=2, column=0, sticky="w", padx=8, pady=4)
    desc_entry = tk.Entry(
        input_frame, font=hw_list.cell_font, width=30, bg="white", fg="black"
    )
    desc_entry.grid(row=3, column=0, padx=8, pady=4)

    tk.Label(
        input_frame,
        text="截止时间 (YYYY-MM-DD):",
        font=hw_list.cell_font,
        bg="#e3ebfc",
        fg="black",
    ).grid(row=4, column=0, sticky="w", padx=8, pady=4)
    deadline_entry = tk.Entry(
        input_frame, font=hw_list.cell_font, width=30, bg="white", fg="black"
    )
    deadline_entry.grid(row=5, column=0, padx=8, pady=4)

    add_btn = tk.Button(
        input_frame,
        text="添加作业",
        command=lambda: add_homework(subject_entry, desc_entry, deadline_entry, scrollable_frame, controller, hw_list),
        font=hw_list.cell_font,
        bg="#4a7abc",
        fg="green",
        relief="flat",
        padx=10,
        pady=4,
    )
    add_btn.grid(row=6, column=0, pady=8)

    # --- Final exam list below ---
    final_exam_list = FinalExamList(scrollable_frame, final_exam_data)
    final_exam_list.pack(pady=30, anchor="w")
