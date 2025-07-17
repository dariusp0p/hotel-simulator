import tkinter as tk
import calendar
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.header = tk.Label(root, text="", font=("Arial", 16))
        self.header.pack(pady=10)

        self.calendar_frame = tk.Frame(root)
        self.calendar_frame.pack()

        nav_frame = tk.Frame(root)
        nav_frame.pack(pady=5)

        tk.Button(nav_frame, text="< Prev", command=self.prev_month).pack(side=tk.LEFT, padx=10)
        tk.Button(nav_frame, text="Next >", command=self.next_month).pack(side=tk.RIGHT, padx=10)

        self.draw_calendar()

    def draw_calendar(self):
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Update header
        self.header.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        # Weekday labels
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold"), padx=10).grid(row=0, column=i)

        # Calendar data
        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)

        for r, week in enumerate(month_calendar, start=1):
            for c, day in enumerate(week):
                text = str(day) if day != 0 else ""
                tk.Label(self.calendar_frame, text=text, padx=10, pady=5).grid(row=r, column=c)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.draw_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.draw_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()