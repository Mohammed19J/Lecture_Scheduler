import tkinter as tk
from tkinter import ttk, messagebox
from datetime import time
import colorsys

class StyledButton(tk.Button):
    def __init__(self, master, **kwargs):
        kwargs.setdefault('font', ('Segoe UI', 12, 'bold'))
        kwargs.setdefault('borderwidth', 0)
        kwargs.setdefault('relief', 'flat')
        kwargs.setdefault('activebackground', kwargs.get('bg', '#4CAF50'))
        super().__init__(master, **kwargs)
        
        self.default_bg = kwargs.get('bg', '#4CAF50')
        self.hover_bg = self.darken_color(self.default_bg)
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_enter(self, e):
        self.configure(bg=self.hover_bg)
    
    def on_leave(self, e):
        self.configure(bg=self.default_bg)
    
    def darken_color(self, hex_color, amount=0.2):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        h, l, s = colorsys.rgb_to_hls(*[x/255.0 for x in rgb])
        new_l = max(0, l - amount)
        new_rgb = colorsys.hls_to_rgb(h, new_l, s)
        
        return '#{:02x}{:02x}{:02x}'.format(
            int(new_rgb[0] * 255), 
            int(new_rgb[1] * 255), 
            int(new_rgb[2] * 255)
        )

class Lecture:
    def __init__(self, name, day, start_time, end_time, lecturer_name, room_number):
        self.name = name
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.lecturer_name = lecturer_name
        self.room_number = room_number

class LectureSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecture Scheduler Pro")
        self.root.geometry("1200x700")  # Increased width to accommodate more content
        self.root.configure(bg='#f0f4f8')
        
        self.lectures_dict = {}
        self.setup_ui()
        
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg='#f0f4f8', padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        left_panel = tk.Frame(main_container, bg='white', 
                              relief=tk.RAISED, borderwidth=1, 
                              width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0,20), pady=(0,20))
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(main_container, bg='white', 
                               relief=tk.RAISED, borderwidth=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=(0,20))
        
        self.create_input_section(left_panel)
        self.random_colors = []
        self.create_lecture_list(right_panel)
        
    def create_input_section(self, parent):
        header = tk.Label(parent, text="Lecture Scheduler", 
                          font=('Segoe UI', 20, 'bold'), 
                          bg='white', fg='#2c3e50', 
                          pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(parent, text="Lecture Name", 
                 font=('Segoe UI', 12), bg='white').pack(anchor='w', padx=20)
        self.lecture_name_entry = tk.Entry(parent, 
                                           font=('Segoe UI', 12), 
                                           width=30, 
                                           relief=tk.FLAT, 
                                           bg='#f1f5f9')
        self.lecture_name_entry.pack(padx=20, pady=(0,10))
        
        tk.Label(parent, text="Lecturer Name", font=('Segoe UI', 12), bg='white').pack(anchor='w', padx=20)
        self.lecturer_name_entry = tk.Entry(parent, font=('Segoe UI', 12), width=30, relief=tk.FLAT, bg='#f1f5f9')
        self.lecturer_name_entry.pack(padx=20, pady=(0,10))
        
        tk.Label(parent, text="Room Number", font=('Segoe UI', 12), bg='white').pack(anchor='w', padx=20)
        self.room_number_entry = tk.Entry(parent, font=('Segoe UI', 12), width=30, relief=tk.FLAT, bg='#f1f5f9')
        self.room_number_entry.pack(padx=20, pady=(0,10))
        
        tk.Label(parent, text="Day", 
                 font=('Segoe UI', 12), bg='white').pack(anchor='w', padx=20)
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.day_var = tk.StringVar(value="Sunday")
        day_dropdown = ttk.Combobox(parent, 
                                    textvariable=self.day_var, 
                                    values=days, 
                                    state="readonly", 
                                    font=('Segoe UI', 12), 
                                    width=27)
        day_dropdown.pack(padx=20, pady=(0,10))
        
        time_frame = tk.Frame(parent, bg='white')
        time_frame.pack(padx=20, pady=(0,10), fill=tk.X)
        
        tk.Label(time_frame, text="Start Time", 
                 font=('Segoe UI', 12), bg='white').pack(anchor='w')
        start_time_frame = tk.Frame(time_frame, bg='white')
        start_time_frame.pack(fill=tk.X)
        
        self.start_hour_var = tk.StringVar(value="09")
        self.start_minute_var = tk.StringVar(value="00")
        
        start_hour_dropdown = ttk.Combobox(start_time_frame, 
                                           textvariable=self.start_hour_var, 
                                           values=[f"{i:02d}" for i in range(24)], 
                                           state="readonly", 
                                           width=5, 
                                           font=('Segoe UI', 12))
        start_hour_dropdown.pack(side=tk.LEFT, padx=(0,5))
        
        start_minute_dropdown = ttk.Combobox(start_time_frame, 
                                             textvariable=self.start_minute_var, 
                                             values=[f"{i:02d}" for i in range(60)], 
                                             state="readonly", 
                                             width=5, 
                                             font=('Segoe UI', 12))
        start_minute_dropdown.pack(side=tk.LEFT)
        
        tk.Label(time_frame, text="End Time", 
                 font=('Segoe UI', 12), bg='white').pack(anchor='w', pady=(10,0))
        end_time_frame = tk.Frame(time_frame, bg='white')
        end_time_frame.pack(fill=tk.X)
        
        self.end_hour_var = tk.StringVar(value="10")
        self.end_minute_var = tk.StringVar(value="00")
        
        end_hour_dropdown = ttk.Combobox(end_time_frame, 
                                         textvariable=self.end_hour_var, 
                                         values=[f"{i:02d}" for i in range(24)], 
                                         state="readonly", 
                                         width=5, 
                                         font=('Segoe UI', 12))
        end_hour_dropdown.pack(side=tk.LEFT, padx=(0,5))
        
        end_minute_dropdown = ttk.Combobox(end_time_frame, 
                                           textvariable=self.end_minute_var, 
                                           values=[f"{i:02d}" for i in range(60)], 
                                           state="readonly", 
                                           width=5, 
                                           font=('Segoe UI', 12))
        end_minute_dropdown.pack(side=tk.LEFT)
        
        add_lecture_btn = StyledButton(parent, 
                                       text="Add Lecture", 
                                       bg='#3498db', 
                                       fg='white', 
                                       command=self.add_lecture)
        add_lecture_btn.pack(pady=20, padx=20, fill=tk.X)
        
        self.status_label = tk.Label(parent, 
                                     text="", 
                                     font=('Segoe UI', 10), 
                                     fg='green', 
                                     bg='white')
        self.status_label.pack(pady=(0,10))
        
        show_schedule_btn = StyledButton(parent, 
                                         text="Generate Schedule", 
                                         bg='#2ecc71', 
                                         fg='white', 
                                         command=self.show_schedule)
        show_schedule_btn.pack(pady=(0,20), padx=20, fill=tk.X)
        
    def create_lecture_list(self, parent):
        list_header = tk.Label(parent, text="Lecture List", 
                               font=('Segoe UI', 16, 'bold'), 
                               bg='white', fg='#2c3e50', 
                               pady=10)
        list_header.pack(fill=tk.X)
        
        list_canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=list_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        list_canvas.configure(yscrollcommand=scrollbar.set)
        list_canvas.bind('<Configure>', lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
        
        self.lecture_list_frame = tk.Frame(list_canvas, bg='white')
        list_canvas.create_window((0, 0), window=self.lecture_list_frame, anchor="nw")
        
    def add_lecture(self):
        lecture_name = self.lecture_name_entry.get().strip()
        if not lecture_name:
            messagebox.showerror("Error", "Please enter a lecture name!")
            return

        try:
            start_t = time(int(self.start_hour_var.get()), int(self.start_minute_var.get()))
            end_t = time(int(self.end_hour_var.get()), int(self.end_minute_var.get()))
        except ValueError:
            messagebox.showerror("Error", "Invalid time selection!")
            return

        if end_t <= start_t:
            messagebox.showerror("Error", "End time must be after start time!")
            return

        lecturer_name = self.lecturer_name_entry.get().strip()
        room_number = self.room_number_entry.get().strip()
        lecture = Lecture(lecture_name, self.day_var.get(), start_t, end_t, lecturer_name, room_number)

        if lecture_name not in self.lectures_dict:
            self.lectures_dict[lecture_name] = []
        self.lectures_dict[lecture_name].append(lecture)

        self.update_lecture_list()
        self.lecture_name_entry.delete(0, tk.END)
        self.lecturer_name_entry.delete(0, tk.END)
        self.room_number_entry.delete(0, tk.END)
        

    def update_lecture_list(self):
        for widget in self.lecture_list_frame.winfo_children():
            widget.destroy()

        for lecture_name, lectures in self.lectures_dict.items():
            for idx, lecture in enumerate(lectures):
                frame = tk.Frame(self.lecture_list_frame, bg='#f1f5f9', padx=10, pady=5)
                frame.pack(fill=tk.X, padx=10, pady=5)

                tk.Label(frame, text=lecture.name, 
                         font=('Segoe UI', 12), 
                         bg='#f1f5f9', width=20, anchor='w').pack(side=tk.LEFT)
                
                tk.Label(frame, text=lecture.day, 
                         font=('Segoe UI', 12), 
                         bg='#f1f5f9', width=10, anchor='w').pack(side=tk.LEFT)
                
                time_str = f"{lecture.start_time.strftime('%H:%M')} - {lecture.end_time.strftime('%H:%M')}, Lecturer: {lecture.lecturer_name}, Room: {lecture.room_number}"
                tk.Label(frame, text=time_str, 
                         font=('Segoe UI', 12), 
                         bg='#f1f5f9', anchor='w').pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
                
                del_btn = StyledButton(frame, text="✕", 
                                       bg='#e74c3c', 
                                       fg='white', 
                                       width=3,
                                       command=lambda n=lecture_name, i=idx: self.delete_lecture(n, i))
                del_btn.pack(side=tk.RIGHT)

    def delete_lecture(self, lecture_name, index):
        if lecture_name in self.lectures_dict:
            if 0 <= index < len(self.lectures_dict[lecture_name]):
                del self.lectures_dict[lecture_name][index]
                if not self.lectures_dict[lecture_name]:
                    del self.lectures_dict[lecture_name]
        self.update_lecture_list()

    def show_schedule(self):
        if not self.lectures_dict:
            messagebox.showwarning("Warning", "No lectures added!")
            return

        schedule = self.calculate_schedules(self.lectures_dict)
        if not schedule:
            messagebox.showerror("Error", "No valid schedule found! Lectures are overlapping.")
        else:
            self.create_calendar(schedule)

    def calculate_schedules(self, lec_dict):
        for lectures in lec_dict.values():
            lectures.sort(key=lambda lec: lec.start_time)

        lectures = list(lec_dict.values())

        current_schedule = []
        optimized_schedule = self.recursive_scheduling(lectures, current_schedule)
        return optimized_schedule

    def recursive_scheduling(self, lecture_options, current_schedule):
        if not any(lecture_options):
            return current_schedule
        current_lecs = lecture_options.pop(0)
        for lecture_option in current_lecs:
            if not any(self.overlap_check(lecture_option, scheduled) for scheduled in current_schedule):
                current_schedule.append(lecture_option)
                result = self.recursive_scheduling(lecture_options, current_schedule)
                if result:
                    return result
                current_schedule.pop()
        lecture_options.insert(0, current_lecs)
        return None

    def overlap_check(self, lec1, lec2):
        if lec1.day != lec2.day:
            return False
        sorted_intervals = sorted([lec1, lec2], key=lambda x: x.start_time)
        return sorted_intervals[0].end_time > sorted_intervals[1].start_time

    def create_calendar(self, schedule):
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Optimized Weekly Schedule")
        schedule_window.geometry("1200x700")
        schedule_window.configure(bg='#f0f4f8')

        canvas = tk.Canvas(schedule_window, bg='#f0f4f8', scrollregion=(0,0,1000,2000))
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(schedule_window, orient=tk.VERTICAL, command=canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = ttk.Scrollbar(schedule_window, orient=tk.HORIZONTAL, command=canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        inner_frame = tk.Frame(canvas, bg='#f0f4f8')
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        style = ttk.Style()
        style.configure("DayHeader.TLabel", font=("Segoe UI", 12, "bold"), background="#dcdcdc", relief="ridge", anchor="center")
        for i, day in enumerate(days):
            ttk.Label(inner_frame, text=day, style="DayHeader.TLabel").grid(row=0, column=i+1, sticky="nsew")

        style.configure("TimeLabel.TLabel", font=("Segoe UI", 10), background="#ebebeb", relief="ridge", anchor="center", width=8)
        for h in range(8,24):
            ttk.Label(inner_frame, text=f"{h:02}:00", style="TimeLabel.TLabel").grid(row=h*2+1, column=0, sticky="nsew")
            ttk.Label(inner_frame, text=f"{h:02}:30", style="TimeLabel.TLabel").grid(row=h*2+2, column=0, sticky="nsew")

        style.configure("Lecture.TLabel", foreground="black", font=("Segoe UI", 10), relief="solid", wraplength=100)
        for lecture in schedule:
            day_index = days.index(lecture.day)

            start_h, start_m = lecture.start_time.hour, lecture.start_time.minute
            end_h, end_m = lecture.end_time.hour, lecture.end_time.minute

            start_row = start_h * 2 + (start_m // 30) + 1
            end_row = end_h * 2 + (end_m // 30) + 1
            row_span = end_row - start_row
            if row_span < 1:
                row_span = 1

            style.configure(f"Lecture_{lecture.name}_{lecture.day}.TLabel", background="#ADD8E6")
            lecture_label = ttk.Label(
                inner_frame,
                text=f"{lecture.name}\n{lecture.start_time.strftime('%H:%M')} - {lecture.end_time.strftime('%H:%M')}\nLecturer: {lecture.lecturer_name}, Room: {lecture.room_number}",
                style=f"Lecture_{lecture.name}_{lecture.day}.TLabel"
            )
            lecture_label.grid(row=start_row, column=day_index+1, rowspan=row_span, sticky="nsew", padx=1, pady=1)

        inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

# Main UI
root = tk.Tk()
app = LectureSchedulerApp(root)
root.mainloop()
