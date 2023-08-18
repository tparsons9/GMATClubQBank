import tkinter as tk 
from PIL import ImageTk, Image
from tkinter import simpledialog, messagebox
import random 
import time
import subprocess
import json 
import numpy as np 
import os

def widget_exists(widget): 
    try: 
        widget.winfo_exists()
        return True
    except: 
        return False 
    

class MyApp(tk.Tk): 
    def __init__(self): 
        super().__init__()
        self.button = tk.Button(self, text = "Open Question Bank", command = self.open_dialog)
        self.button.pack()
    def open_dialog(self): 
        self.dialog = CustomDialog(self, "Question Bank")

class CustomDialog(simpledialog.Dialog): 
     
    def __init__(self, parent, title): 
        self.data_loader()
        self.parent = parent
        self.paused = True
        self.start_time = None
        self.try_counter = 0 
        self.timer_running = False
        self.is_correct = False
        self.calc = tk.PhotoImage(file = r'calculator.png')
        self.url_img = tk.PhotoImage(file = r'url.png')
        self.bm = tk.PhotoImage(file = r'bookmark.png')
        self.bm2 = tk.PhotoImage(file = r'bookmark2.png')
        self.bm_image = self.toggle_bookmark_img() 
        self.parent = parent
        self.result = None
        super().__init__(parent, title)

    
    def data_loader(self): 
        with open("question_dict.json", "r") as f: 
            self.questions = json.load(f)
        
        for key in self.questions: #convert str to int 
            self.questions[key]['attempts'] = {int(k): v for k, v in self.questions[key]['attempts'].items()}
        
        min_attempts = min([np.max([a for a in q['attempts'].keys()] or [float('-inf')]) for q in self.questions.values()])
        self.unseen_questions = []
        for k, v in self.questions.items(): 
            if min_attempts == float('-inf') and v['attempts'] == {}: 
                self.unseen_questions.append(k)
            elif v['bookmarked'] == 1: 
                self.unseen_questions.append(k)
            elif max(list(v['attempts'].keys())) == min_attempts: 
                self.unseen_questions.append(k)
        
        imgs = [i.split('_')[1].replace('.png', '') for i in os.listdir('screenshots')]
        self.unseen_questions = [i for i in self.unseen_questions if i in imgs]
        self.idx = random.choice(self.unseen_questions)
        self.unseen_questions.remove(self.idx)
        self.current_question_idx = str(random.randint(0, len(self.questions) - 1))
        self.image_path = f"screenshots/question_{self.idx}.png"

    def resize_image(self, image): 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if image.width>screen_width or image.height>screen_height: 
            if image.width/screen_width > image.height/screen_height: 
                new_width = screen_width
                new_height = int(image.height * screen_width/image.width)
            else: 
                new_height = screen_height
                new_width = int(image.width)
            image = image.resize((new_width, new_height), Image.LANCZOS)
        return image
    
    def toggle_bookmark_img(self):
        img = self.bm2 if self.questions[self.idx]['bookmarked'] == 0 else self.bm
        return img
    
    def convert_time(self, time_taken): 
        minutes = int(time_taken // 60)
        seconds = int(time_taken % 60)
        return f"{minutes}:{seconds:02d}"
        
        
    def body(self, master): 
        self.image = Image.open(self.image_path)
        self.image = self.resize_image(self.image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(master, image = self.photo)
        self.label.pack()

        self.question_label = tk.Label(master, text = f"Question {self.idx}")
        self.question_label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.next_button = tk.Button(master, text = "Next", command = self.next_question, width = 10, padx=5, pady=5)
        self.next_button.pack()

        self.start_button = tk.Button(master, text = "Start Timer", command = self.start_timer, width = 10, padx=5, pady=5)
        self.start_button.pack()

        self.timer_label = tk.Label(master, text = "0:00")
        self.timer_label.pack()

        self.button = tk.Button(self, command = self.open_calculator, image = self.calc)
        self.button.pack()

        self.bookmark = tk.Button(self, command = self.log_bookmark, image = self.bm_image)
        self.bookmark.pack(anchor = tk.SE, side = tk.BOTTOM)
        self.url = tk.Button(self, command = self.open_url, image = self.url_img)
        self.url.pack(anchor = tk.SE, side = tk.BOTTOM)
        self.bookmark.place(relx = 1.0, rely = 1.0, anchor = tk.SE)
        self.button.place(relx = 0.9, rely = 1.0, anchor = tk.SE)
        self.url.place(relx = 0.8, rely = 1.0, anchor = tk.SE)
        self.calculator_open = False 

        return self.entry 
    
    def buttonbox(self): 
        box = tk.Frame(self)
        self.ok_button = tk.Button(box, text = "OK", width = 10, command = self.ok_button_pressed, default = tk.ACTIVE)
        self.ok_button.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.cancel_button = tk.Button(box, text = "Quit", width = 10, command = self.cancel_button_pressed)
        self.cancel_button.pack(side = tk.LEFT, padx = 5, pady = 5)
        #self.bind("<Return>", lambda event: self.ok_button_pressed())
        #self.bind("<Escape>", lambda event: self.cancel_button_pressed())
        box.pack()
    
    def next_question(self): 
        if self.winfo_exists(): 
            self.idx = random.choice(self.unseen_questions)
            self.unseen_questions.remove(self.idx)
            self.image_path = f"screenshots/question_{self.idx}.png"
            self.label.config(image="")
            self.question_label.configure(text = f"Question {self.idx}")
            self.image = Image.open(self.image_path)
            self.image = self.resize_image(self.image)
            self.photo = ImageTk.PhotoImage(self.image)
            self.label.configure(image = self.photo)
            self.entry.delete(0, tk.END)
            self.entry.focus_set()
            self.entry.config(state='normal')
            self.ok_button.config(state = 'normal')
            self.try_counter = 0 
            self.start_time = None
            self.timer_running = False
            self.pause_time = None
            self.start_button.config(text = "Start Timer")
            self.ok_button.config(state = 'disabled')
            self.timer_label.config(text = "0:00")
            self.bm_image = self.toggle_bookmark_img()
            self.bookmark.config(image = self.bm_image)

    def start_timer(self):
        if not self.timer_running: 
            self.timer_running = True
            if self.start_time is None: 
                self.start_time = time.time()
            else:
                self.start_time += time.time() - self.pause_time
            self.update_timer()
            self.start_button.config(text = "Pause")
            self.ok_button.config(state = 'normal')
        else:
            self.timer_running = False
            self.pause_time = time.time()
            self.start_button.config(text = "Resume")
            self.ok_button.config(state = 'disabled')
    
    def log_bookmark(self): 
        if self.questions[self.idx]['bookmarked'] == 0: 
            self.questions[self.idx]['bookmarked'] = 1
            self.bm_image = self.bm
        else: 
            self.questions[self.idx]['bookmarked'] = 0
            self.bm_image = self.bm2
        self.bookmark.config(image = self.bm_image)
        
    def update_timer(self): 
        if self.timer_running: 
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text = self.convert_time(elapsed_time))
            self.after(1000, self.update_timer)
    
    def open_url(self):
        url = self.questions[self.idx]['href']
        subprocess.run(['open', url])
    
    def open_calculator(self): 
        if self.calculator_open: 
            self.calculator_open = False
            subprocess.run(['pkill', '-x', 'Calculator'])
        else:
            self.calculator_open = True
            subprocess.Popen(['open', '-a', 'Calculator'])
    
    def ok_button_pressed(self): 
        self.result = self.entry.get()
        self.elapsed_time = time.time() - self.start_time
        if self.result == self.questions[self.idx]['answer']:
            self.id = self.idx 
            self.handle_correct_answer()
            
        else: 
            self.handle_incorrect_answer()
    
    def handle_correct_answer(self): 
        self.try_counter += 1
        self.grab_release()
        self.notes_window = TopMessageWindow(self, "You got the correct answer!", f"Time Taken: {self.convert_time(self.elapsed_time)}", self.questions[self.idx])
        self.notes_window.wait_window()
        #self.process_notes_window_result(notes_window)
        
            
        
    
    def process_notes_and_update(self, saved_notes, bookmark_): 
        new_attempt = str(int(list(self.questions[self.idx]['attempts'])[-1])) if self.questions[self.idx]['attempts'] != {} else '1'
        self.questions[self.idx]['attempts'][new_attempt] = {'tries': self.try_counter, 'time_taken': self.convert_time(self.elapsed_time), 'notes': saved_notes}
        self.questions[self.idx]['bookmarked'] = bookmark_
        self.grab_set()
        
    
    def handle_incorrect_answer(self):
        self.try_counter += 1
        self.timer_running = False 
        messagebox.showinfo("Incorrect", f"Your answer is incorrect. Please try again.")
        self.timer_running = True

    def cancel_button_pressed(self): 
        with open("question_dict.json", "w") as f: 
            json.dump(self.questions, f, indent = 4)
            f.flush()
            os.fsync(f.fileno())
        self.grab_release()
        self.destroy()
            

class TopMessageWindow(tk.Toplevel): 
    def __init__(self, parent, title, message, question): 
        super().__init__(parent)
        self.title(title)
        self.geometry("600x300")
        self.question = question
        self.bookmarked = question['bookmarked']
        self.bm = tk.PhotoImage(file = r'bookmark.png')
        self.bm2 = tk.PhotoImage(file = r'bookmark2.png')
        self.url = tk.PhotoImage(file = r'url.png')
        self.label = tk.Label(self, text = message)
        self.label.pack(pady=10)
        self.notes_label = tk.Label(self, text="Notes: ")
        self.notes_label.pack(pady=10)
        self.notes_entry = tk.Text(self, height=10, width=40)
        self.notes_entry.pack(pady=10)
        self.url_button = tk.Button(self, command=self.open_url, image=self.url)
        self.url_button.pack(anchor = tk.SE, side = tk.BOTTOM)
        self.url_button.place(relx = 0.9, rely = 1.0, anchor = tk.SE)
        self.bookmark_button = tk.Button(self, command=self.log_bookmark, image=self.toggle_bookmark_img())
        self.bookmark_button.pack(anchor = tk.SE, side = tk.BOTTOM)
        self.bookmark_button.place(relx = 1.0, rely = 1.0, anchor = tk.SE)
        self.saved_notes = "" 
        self.save_note_button = tk.Button(self, text="Save Notes", command=self.save_notes)
        self.save_note_button.pack(side = tk.BOTTOM, padx = 5, pady = 5)
        self.review_button = tk.Button(self, text="Review", command=self.review, height = 5)
        self.review_button.pack(anchor = tk.SW, side = tk.LEFT, padx = 5)
    def toggle_bookmark_img(self):
        img = self.bm2 if self.bookmarked == 0 else self.bm
        return img
     
    def log_bookmark(self): 
        self.bookmarked = 1 if self.bookmarked == 0 else 0
        self.bookmark_button.config(self.toggle_bookmark_img())
    
    def review(self):
        old_notes = []
        for k, v in self.question['attempts'].items(): 
            old_notes.append(f"Attempt {k}: {v['notes']}")
        if old_notes != []: 
            messagebox.showinfo("Review", "\n".join(old_notes))
        else:
            messagebox.showinfo("Review", "No previous attempts")

    def open_url(self):
        url = self.question['href']
        subprocess.run(['open', url])
    
    def save_notes(self): 
        self.saved_notes = self.notes_entry.get("1.0", tk.END).strip()
        self.master.process_notes_and_update(self.saved_notes, self.bookmarked)
        self.master.next_question()
        self.destroy()
    
        
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
