import tkinter as tk
from PIL import Image, ImageTk
import webview
from datetime import datetime, timedelta
import tkinter.messagebox as messagebox

import tkinter as tk
from datetime import datetime

class FinalExamList(tk.Frame):
    def __init__(self, parent, exam_data):
        super().__init__(parent, bg="white", highlightbackground="#4a7abc", highlightthickness=2)

        self.cell_font = ("Arial", 12)
        self.exam_data = exam_data

        # Headers
        headers = ["#", "科目", "考试日期", "倒计时"]
        widths = [30, 150, 180, 120]  

        for col, (header, width) in enumerate(zip(headers, widths)):
            label = tk.Label(self, text=header, font=("Arial", 12, "bold"), bg="#4a7abc", fg="white", width=width//10)
            label.grid(row=0, column=col, sticky="nsew", padx=2, pady=4)

        
        for i, exam in enumerate(exam_data, start=1):
            
            num_label = tk.Label(self, text=str(i), font=self.cell_font, bg="white", fg="black")
            num_label.grid(row=i, column=0, sticky="w", padx=2, pady=2)

            
            subject_label = tk.Label(self, text=exam["subject"], font=self.cell_font, bg="white", fg="blue")
            subject_label.grid(row=i, column=1, sticky="w", padx=2, pady=2)

            
            date_str = exam["exam_date"].strftime("%Y-%m-%d %H:%M")
            date_label = tk.Label(self, text=date_str, font=self.cell_font, bg="#e3ebfc", fg="blue")
            date_label.grid(row=i, column=2, sticky="w", padx=2, pady=2)

            countdown_label = tk.Label(self, font=self.cell_font, bg="white", fg="red")
            countdown_label.grid(row=i, column=3, sticky="w", padx=2, pady=2)

          
            exam["countdown_label"] = countdown_label

        self.update_timers()

    def update_timers(self):
        now = datetime.now()
        for exam in self.exam_data:
            delta = exam["exam_date"] - now
            label = exam.get("countdown_label")
            if delta.total_seconds() > 0:
                days = delta.days
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                label.config(text=f"{days}天 {hours:02}:{minutes:02}:{seconds:02}")
            else:
                label.config(text="考试已结束")

        self.after(1000, self.update_timers)



def open_web_window(url):
    webview.create_window("Website", url, width=800, height=600)
    webview.start()


def create_rounded_block(parent, x, y, w=300, h=150, r=20, color="gray", image_path=None,
                         open_window=None, text=None, text_color="black", font=("Helvetica", 25)):
    canvas = tk.Canvas(parent, width=w, height=h, bg="white", highlightthickness=0)
    canvas.place(x=x, y=y)

    # Your original drawing code unchanged:
    canvas.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=color, outline=color)
    canvas.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=color, outline=color)
    canvas.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill=color, outline=color)
    canvas.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle((r, 0, w-r, h), fill=color, outline=color)
    canvas.create_rectangle((0, r, w, h-r), fill=color, outline=color)      

    if image_path:
        img = Image.open(image_path)
        img = img.resize((50, 50), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        canvas.image = photo  
        canvas.create_image(120, 20, image=photo, anchor='nw')

    if text:
        canvas.create_text(w//2, h//2 + 30, text=text, fill=text_color, font=font, anchor='center')    

    if open_window:
        canvas.bind("<Button-1>", lambda event: open_window())

    # Animation variables:
    animation_steps = 10
    animation_delay = 20  # milliseconds
    move_distance = 7

    def animate_move(step=0, direction=1):
        # direction=1 means move up, -1 means move down
        if step <= animation_steps:
            current_y = canvas.winfo_y()
            dy = direction * (move_distance / animation_steps)
            new_y = current_y - dy  # minus because moving up reduces y coordinate
            canvas.place_configure(y=int(new_y))
            canvas.after(animation_delay, animate_move, step + 1, direction)
        else:
            # Ensure final position is exact
            if direction == 1:
                canvas.place_configure(y=y - move_distance)
            else:
                canvas.place_configure(y=y)

    def on_enter(event):
        canvas.config(cursor="hand2")
        animate_move(direction=1)

    def on_leave(event):
        canvas.config(cursor="")
        animate_move(direction=-1)

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    return canvas


app1 = tk.Tk()

app1.geometry("1920x1080")
app1.title("Group Project")
app1["bg"] = "white"

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
x_positions = [
    spacing,
    spacing * 2 + block_width,
    spacing * 3 + block_width * 2
]


create_rounded_block(app1, x=x_positions[0], y=150, color="#e3ebfc", image_path="pku.svg.png", open_window=lambda: open_web_window("https://www.pku.edu.cn"), text="PKU Canvas")
create_rounded_block(app1, x=x_positions[1], y=150, color="#e3ebfc", image_path="poj.png", open_window=lambda: open_web_window("https://www.pku.edu.cn"), text="OpenJudge")
create_rounded_block(app1, x=x_positions[2], y=150, color="#e3ebfc", image_path="jxw.png", open_window=lambda: open_web_window("https://www.pku.edu.cn"), text="北京大学教学网")

class HomeworkList(tk.Frame):
    def __init__(self, parent, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data = data
        self.columns = ['#', '科目', '作业描述', '截止时间']

        self.header_font = ("Helvetica", 14, "bold")
        self.cell_font = ("Helvetica", 12)
        self.deadline_font = ("Helvetica", 11, "italic")
        self.countdown_font = ("Helvetica", 10)

        self.create_widgets()
        self.update_countdowns()

    def create_widgets(self):
        # header row
        for col, text in enumerate(self.columns):
            label = tk.Label(self, text=text, font=self.header_font, borderwidth=2, relief="ridge", bg="#4a7abc", fg="white", padx=8, pady=6)
            label.grid(row=0, column=col, sticky="nsew")

        # columns
        self.grid_columnconfigure(0, weight=1, minsize=40)   # # column
        self.grid_columnconfigure(1, weight=3, minsize=120)  # Subject
        self.grid_columnconfigure(2, weight=5, minsize=300)  # Description
        self.grid_columnconfigure(3, weight=3, minsize=180)  # Deadline

        # Create rows of homework data
        self.countdown_labels = []
        for i, row in enumerate(self.data, start=1):
            # Number column
            num_lbl = tk.Label(self, text=str(i), font=self.cell_font, borderwidth=1, relief="solid", padx=6, pady=4, bg="white", fg="black")
            num_lbl.grid(row=i, column=0, sticky="nsew")

            # Subject column
            subj_lbl = tk.Label(self, text=row['subject'], font=self.cell_font, borderwidth=1, relief="solid", padx=6, pady=4)
            subj_lbl.grid(row=i, column=1, sticky="nsew")

            # Description column
            desc_lbl = tk.Label(self, text=row['description'], font=self.cell_font, borderwidth=1, relief="solid", padx=6, pady=4, wraplength=280, justify="left")
            desc_lbl.grid(row=i, column=2, sticky="nsew")

            # Deadline column (two lines: date and countdown)
            deadline_str = row['deadline'].strftime("%d %b %Y")
            deadline_lbl = tk.Label(self, text=deadline_str, font=self.deadline_font, borderwidth=0, relief="flat", padx=6, pady=2, fg="#a00", anchor="n", bg="#e3ebfc")
            deadline_lbl.grid(row=i, column=3, sticky="nsew")

            countdown_lbl = tk.Label(self, font=self.countdown_font, borderwidth=0, relief="flat", padx=6, pady=2, fg="#007700", bg="#e3ebfc")
            countdown_lbl.grid(row=i, column=3, sticky="nsew", pady=(28, 6))  # placed below deadline label with padding

            self.countdown_labels.append((countdown_lbl, row['deadline']))

    def update_countdowns(self):
        now = datetime.now()
        for lbl, deadline in self.countdown_labels:
            diff = deadline - now
            if diff.total_seconds() > 0:
                days = diff.days
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                countdown_text = f"{days}d {hours}h {minutes}m {seconds}s left"
                lbl.config(text=countdown_text, fg="#007700")
            else:
                lbl.config(text="Deadline passed", fg="#aa0000")
        self.after(1000, self.update_countdowns)  # update every second

# homework_data = [
#     {"subject": "Math", "description": "Complete exercises 5 to 10 on page 123.", "deadline": datetime(2025, 5, 29, 23, 59, 59)},
#     {"subject": "Physics", "description": "Prepare lab report on thermodynamics.", "deadline": datetime(2025, 5, 28, 18, 0, 0)},
#     {"subject": "History", "description": "Write a 1000-word essay about World War II.", "deadline": datetime(2025, 6, 1, 12, 0, 0)},
#     {"subject": "English", "description": "Read chapters 4 and 5 and answer the questions.", "deadline": datetime(2025, 5, 30, 15, 30, 0)},
# ]

# final_exam_data = [
#     {"subject": "数学", "exam_date": datetime(2025, 6, 15, 9, 0)},
#     {"subject": "英语", "exam_date": datetime(2025, 6, 18, 13, 30)},
#     {"subject": "物理", "exam_date": datetime(2025, 6, 20, 8, 0)},
# ]

homework_data = 


hw_list = HomeworkList(app1, homework_data)
hw_list.place(x=225, y=350)



def get_final_exam_y():
    return 350 + len(homework_data) * 45 + 60

hw_list.update_idletasks() 
hw_list_width = hw_list.winfo_width()
hw_list_x = 225 

# --- Input section to add new homework ---
input_frame = tk.Frame(app1, bg="#e3ebfc", highlightbackground="#4a7abc", highlightthickness=2)
gap = 20
input_frame.place(x=hw_list_x + hw_list_width + gap, y=350)
# Labels and entries
tk.Label(input_frame, text="科目:", font=hw_list.cell_font, bg="#e3ebfc", fg="black").grid(row=0, column=0, sticky="w", padx=8, pady=4)
subject_entry = tk.Entry(input_frame, font=hw_list.cell_font, width=30, bg="white", fg="black")
subject_entry.grid(row=1, column=0, padx=8, pady=4)

tk.Label(input_frame, text="描述:", font=hw_list.cell_font, bg="#e3ebfc", fg="black").grid(row=2, column=0, sticky="w", padx=8, pady=4)
desc_entry = tk.Entry(input_frame, font=hw_list.cell_font, width=30, bg="white", fg="black")
desc_entry.grid(row=3, column=0, padx=8, pady=4)

tk.Label(input_frame, text="截止时间 (YYYY-MM-DD HH:MM):", font=hw_list.cell_font, bg="#e3ebfc", fg="black").grid(row=4, column=0, sticky="w", padx=8, pady=4)
deadline_entry = tk.Entry(input_frame, font=hw_list.cell_font, width=30, bg="white", fg="black")
deadline_entry.grid(row=5, column=0, padx=8, pady=4)

def get_homework_list_height():
    return 350 + len(homework_data) * 45


def add_homework():
    global hw_list
    subject = subject_entry.get().strip()
    desc = desc_entry.get().strip()
    deadline_str = deadline_entry.get().strip()

    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
    except ValueError:
        tk.messagebox.showerror("格式错误", "请使用正确的时间格式: YYYY-MM-DD HH:MM")
        return

    if subject and desc and deadline:
        homework_data.append({
            "subject": subject,
            "description": desc,
            "deadline": deadline
        })

        hw_list.destroy()  # Re-render the list
        new_hw_list = HomeworkList(app1, homework_data)
        new_hw_list.place(x=225, y=350)

        hw_list = new_hw_list

        subject_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)

add_btn = tk.Button(input_frame, text="添加作业", command=add_homework, font=hw_list.cell_font, bg="#4a7abc", fg="green", relief="flat", padx=10, pady=4)
add_btn.grid(row=6, column=0, pady=8)

final_exam_list = FinalExamList(app1, final_exam_data)
final_exam_list.place(x=225, y=get_final_exam_y() )


app1.mainloop()
