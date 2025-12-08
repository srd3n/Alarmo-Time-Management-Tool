import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from modules.alarmManager import AlarmManager
from modules.timeUtils import TimeChecker
from modules.soundPlayer import play_alarm_sound
import threading
from datetime import datetime
import os

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
class AlarmoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarmo - Time Management Tool")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg="#f0f0f0")
        self.root.geometry(f"+{int(self.root.winfo_screenwidth()/2 - WINDOW_WIDTH/2)}+{int(self.root.winfo_screenheight()/2 - WINDOW_HEIGHT/2)}")

        self.alarm_manager = AlarmManager()
        self.time_checker = TimeChecker()
        self.selected_alarm_id = None
        self.running = True
        self.check_thread = threading.Thread(target=self._check_alarms_loop, daemon=True)
        self.check_thread.start()
        
        self._create_widgets()
        self._refresh_alarm_list()
    
    def _create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        left_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        title_frame = tk.Frame(left_frame, bg="#ffffff")
        title_frame.pack(pady=20)
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logo_path = os.path.join(base_dir, "assets", "assets", "sounds", "2227930.png")
            
            if os.path.exists(logo_path):
                logo_image = tk.PhotoImage(file=logo_path)
                logo_image = logo_image.subsample(8, 8)
                self.logo_image = logo_image
            else:
                logo_path_rel = os.path.join("assets", "assets", "sounds", "2227930.png")
                if os.path.exists(logo_path_rel):
                    logo_image = tk.PhotoImage(file=logo_path_rel)
                    logo_image = logo_image.subsample(8, 8)
                    self.logo_image = logo_image
                else:
                    logo_image = None
        except Exception as e:
            print(f"Could not load logo image: {e}")
            logo_image = None
        if logo_image:
            bell_label = tk.Label(
                title_frame,
                image=logo_image,
                bg="#ffffff"
            )
            bell_label.pack(side=tk.LEFT, padx=(10, 10))
        else:
            bell_label = tk.Label(
                title_frame,
                text="🔔",
                font=("Arial", 28),
                bg="#ffffff"
            )
            bell_label.pack(side=tk.LEFT, padx=(10, 10))
        title_label = tk.Label(
            title_frame, 
            text="Alarmo", 
            font=("Arial", 28, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        title_label.pack(side=tk.LEFT, padx=10)
        time_frame = tk.Frame(left_frame, bg="#ffffff")
        time_frame.pack(pady=20)
        tk.Label(time_frame, text="hour", font=("Arial", 14, "bold"), bg="#ffffff").grid(row=0, column=0, padx=5)
        self.hour_var = tk.StringVar(value="06")
        hour_entry = tk.Entry(time_frame, textvariable=self.hour_var, width=10, font=("Arial", 16), 
                             bg="#e0e0e0", relief=tk.SUNKEN, borderwidth=2)
        hour_entry.grid(row=1, column=0, padx=5, pady=5)
        tk.Label(time_frame, text="min", font=("Arial", 14, "bold"), bg="#ffffff").grid(row=0, column=1, padx=5)
        self.minute_var = tk.StringVar(value="00")
        minute_entry = tk.Entry(time_frame, textvariable=self.minute_var, width=10, font=("Arial", 16),
                               bg="#e0e0e0", relief=tk.SUNKEN, borderwidth=2)
        minute_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(time_frame, text="sec", font=("Arial", 14, "bold"), bg="#ffffff").grid(row=0, column=2, padx=5)
        self.second_var = tk.StringVar(value="00")
        second_entry = tk.Entry(time_frame, textvariable=self.second_var, width=10, font=("Arial", 16),
                               bg="#e0e0e0", relief=tk.SUNKEN, borderwidth=2)
        second_entry.grid(row=1, column=2, padx=5, pady=5)
        tk.Label(time_frame, text="period", font=("Arial", 14, "bold"), bg="#ffffff").grid(row=0, column=3, padx=5)
        self.period_var = tk.StringVar(value="AM")
        period_menu = tk.OptionMenu(time_frame, self.period_var, "AM", "PM")
        period_menu.config(width=8, font=("Arial", 16), bg="#e0e0e0", relief=tk.SUNKEN, borderwidth=2)
        period_menu.grid(row=1, column=3, padx=5, pady=5)
        note_frame = tk.Frame(left_frame, bg="#ffffff")
        note_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(note_frame, text="note", font=("Arial", 14, "bold"), bg="#ffffff").pack(anchor=tk.W)
        self.note_text = scrolledtext.ScrolledText(
            note_frame, 
            height=8, 
            width=30,
            font=("Arial", 14),
            bg="#e0e0e0",
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.note_text.pack(fill=tk.BOTH, expand=True, pady=5)
        add_button = tk.Button(
            left_frame,
            text="ADD ALARM",
            command=self._add_alarm,
            font=("Arial", 18, "bold"),
            bg="#FFD700",
            fg="#000000",
            relief=tk.RAISED,
            borderwidth=3,
            padx=30,
            pady=15,
            cursor="hand2"
        )
        add_button.pack(pady=20)
        right_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        title_label_right = tk.Label(
            right_frame,
            text="Active Alarms",
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            fg="#333333"
        )
        title_label_right.pack(pady=20)
        button_frame = tk.Frame(right_frame, bg="#ffffff")
        button_frame.pack(pady=10)
        
        delete_button = tk.Button(
            button_frame,
            text="DELETE",
            command=self._delete_alarm,
            font=("Arial", 14, "bold"),
            bg="#FFD700",
            fg="#000000",
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        update_button = tk.Button(
            button_frame,
            text="UPDATE",
            command=self._update_alarm,
            font=("Arial", 14, "bold"),
            bg="#FFD700",
            fg="#000000",
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        update_button.pack(side=tk.LEFT, padx=5)
        
        history_button = tk.Button(
            button_frame,
            text="HISTORY",
            command=self._show_history,
            font=("Arial", 14, "bold"),
            bg="#FFD700",
            fg="#000000",
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        history_button.pack(side=tk.LEFT, padx=5)
        list_frame = tk.Frame(right_frame, bg="#ffffff")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.alarm_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 14),
            bg="#e0e0e0",
            relief=tk.SUNKEN,
            borderwidth=2,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            height=15
        )
        self.alarm_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.alarm_listbox.bind('<<ListboxSelect>>', self._on_alarm_select)
        
        scrollbar.config(command=self.alarm_listbox.yview)
    
    def _add_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            second = int(self.second_var.get())
            period = self.period_var.get()
            note = self.note_text.get("1.0", tk.END).strip()
            if not (0 <= hour <= 12):
                messagebox.showerror("Error", "Hour must be between 0 and 12")
                return
            if not (0 <= minute <= 59):
                messagebox.showerror("Error", "Minute must be between 0 and 59")
                return
            if not (0 <= second <= 59):
                messagebox.showerror("Error", "Second must be between 0 and 59")
                return
            if hour == 0:
                hour = 12
            self.alarm_manager.create_alarm(hour, minute, second, period, note)
            self._refresh_alarm_list()
            self._clear_inputs()
            messagebox.showinfo("Success", "Alarm added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for time")
    
    def _delete_alarm(self):
        if self.selected_alarm_id is None:
            messagebox.showwarning("Warning", "Please select an alarm to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this alarm?"):
            self.alarm_manager.delete_alarm(self.selected_alarm_id)
            self.selected_alarm_id = None
            self._refresh_alarm_list()
            messagebox.showinfo("Success", "Alarm deleted successfully!")
    
    def _update_alarm(self):
        if self.selected_alarm_id is None:
            messagebox.showwarning("Warning", "Please select an alarm to update")
            return
        
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            second = int(self.second_var.get())
            period = self.period_var.get()
            note = self.note_text.get("1.0", tk.END).strip()
            if not (0 <= hour <= 12):
                messagebox.showerror("Error", "Hour must be between 0 and 12")
                return
            if not (0 <= minute <= 59):
                messagebox.showerror("Error", "Minute must be between 0 and 59")
                return
            if not (0 <= second <= 59):
                messagebox.showerror("Error", "Second must be between 0 and 59")
                return
            if hour == 0:
                hour = 12
            self.alarm_manager.update_alarm(
                self.selected_alarm_id,
                hour=hour,
                minute=minute,
                second=second,
                period=period,
                note=note
            )
            self._refresh_alarm_list()
            self.selected_alarm_id = None
            self._clear_inputs()
            messagebox.showinfo("Success", "Alarm updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for time")
    
    def _show_history(self):
        history = self.alarm_manager.get_history()
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Alarm History")
        history_window.geometry("500x400")
        
        history_text = scrolledtext.ScrolledText(history_window, font=("Arial", 10))
        history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if not history:
            history_text.insert(tk.END, "No alarm history available.")
        else:
            for alarm in reversed(history):
                time_str = self.alarm_manager.format_alarm_time(alarm)
                note = alarm.get('note', 'No note')
                deleted_at = alarm.get('deleted_at', 'Unknown')
                history_text.insert(tk.END, f"{time_str} - {note}\n")
                history_text.insert(tk.END, f"  Deleted: {deleted_at}\n\n")
        
        history_text.config(state=tk.DISABLED)
    
    def _on_alarm_select(self, event):
        selection = self.alarm_listbox.curselection()
        if selection:
            index = selection[0]
            alarms = self.alarm_manager.read_alarms()
            if index < len(alarms):
                alarm = alarms[index]
                self.selected_alarm_id = alarm['id']
                self._load_alarm_to_form(alarm)
    
    def _load_alarm_to_form(self, alarm):
        self.hour_var.set(str(alarm.get('hour_12', alarm.get('hour', 0))))
        self.minute_var.set(str(alarm.get('minute', 0)))
        self.second_var.set(str(alarm.get('second', 0)))
        self.period_var.set(alarm.get('period', 'AM'))
        self.note_text.delete("1.0", tk.END)
        self.note_text.insert("1.0", alarm.get('note', ''))
    
    def _clear_inputs(self):
        self.hour_var.set("06")
        self.minute_var.set("00")
        self.second_var.set("00")
        self.period_var.set("AM")
        self.note_text.delete("1.0", tk.END)
    
    def _refresh_alarm_list(self):
        self.alarm_listbox.delete(0, tk.END)
        alarms = self.alarm_manager.read_alarms()
        
        for alarm in alarms:
            time_str = self.alarm_manager.format_alarm_time(alarm)
            note = alarm.get('note', 'No note')
            display_text = f"{time_str} {note}"
            self.alarm_listbox.insert(tk.END, display_text)
    
    def _check_alarms_loop(self):
        import time
        while self.running:
            try:
                alarms = self.alarm_manager.read_alarms()
                triggered = self.time_checker.check_alarms(alarms)
                for alarm in triggered:
                    play_alarm_sound()
                    self.root.after(0, lambda a=alarm: self._show_alarm_notification(a))
                time.sleep(1)
            except Exception as e:
                print(f"Error checking alarms: {e}")
                time.sleep(1)
    
    def _show_alarm_notification(self, alarm):
        time_str = self.alarm_manager.format_alarm_time(alarm)
        note = alarm.get('note', 'No note')
        messagebox.showinfo("Alarm!", f"{time_str}\n{note}")
    
    def on_closing(self):
        self.running = False
        self.root.destroy()

