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
    label = tk.Label(
        app1,
        text="选择教学平台",
        font=("Helvetica", 38, "bold"),
        fg="black",
        bg="white",
        padx=20,
        pady=30,
    )
    label.pack()

    block_width = 150
    spacing = (1920 - 3 * block_width) // 6.5
    x_positions = [spacing, spacing * 2 + block_width, spacing * 3 + block_width * 2]

    create_rounded_block(
        app1,
        x=x_positions[0],
        y=150,
        color="#e3ebfc",
        image_path="assets/pku.png",
        open_window=lambda: open_web_window("https://www.pku.edu.cn"),
        text="PKU Canvas",
    )
    create_rounded_block(
        app1,
        x=x_positions[1],
        y=150,
        color="#e3ebfc",
        image_path="assets/poj.png",
        open_window=lambda: open_web_window("https://www.pku.edu.cn"),
        text="OpenJudge",
    )
    create_rounded_block(
        app1,
        x=x_positions[2],
        y=150,
        color="#e3ebfc",
        image_path="assets/jxw.png",
        open_window=lambda: open_web_window("https://www.pku.edu.cn"),
        text="北京大学教学网",
    )
    
    raw_homework_data = controller.load_assignments()
    homework_data = [
        {
            "subject": item[0],
            "description": item[1],
            "deadline": datetime.strptime(item[2], "%Y-%m-%d"),
        }
        for item in raw_homework_data
    ]
    
    raw_final_exam_data = controller.load_exams()
    final_exam_data = [
        {"subject": item[0], "exam_date": datetime.strptime(item[1], "%Y-%m-%d")}
        for item in raw_final_exam_data
    ]

    hw_list = HomeworkList(app1, homework_data)
    hw_list.place(x=225, y=350)

    hw_list.update_idletasks()
    hw_list_width = hw_list.winfo_width()
    hw_list_x = 225

    # --- Input section to add new homework ---
    input_frame = tk.Frame(
        app1, bg="#e3ebfc", highlightbackground="#4a7abc", highlightthickness=2
    )
    gap = 20
    input_frame.place(x=hw_list_x + hw_list_width + gap, y=350)
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
        command=lambda: add_homework(subject_entry, desc_entry, deadline_entry, app1, controller, hw_list),
        font=hw_list.cell_font,
        bg="#4a7abc",
        fg="green",
        relief="flat",
        padx=10,
        pady=4,
    )
    add_btn.grid(row=6, column=0, pady=8)

    final_exam_list = FinalExamList(app1, final_exam_data)
    final_exam_list.place(x=225, y=get_final_exam_y(homework_data))
