from tkinter import *
from tkinter.simpledialog import askstring
from tkinter import messagebox
from Class import *
import sys

# --- Ask for Receiver Email ---
receiver_email = askstring("Receiver Email", "Enter the receiver's email:")
if receiver_email is None: # if click cancel exit program
    sys.exit()
while receiver_email == "": # ki madakhalch email may3adich
    messagebox.showwarning("Missing Email", "You must enter a receiver email.")
    receiver_email = askstring("Receiver Email", "Enter the receiver's email:")
    if receiver_email is None:# if click cancel exit program
        sys.exit()

# --- Exit Program ---
def exit_program():
    window.quit()

# --- Create GUI Window ---
window = Tk()
window.title("Fire and Human Detection")
window.geometry("1280x720")
window.resizable(False, False)
window.configure(bg="white")

# --- Title Label ---
title = Label(window, text="Fire and Human Detection",
                font=("Arial", 30, "bold"),
                bg="white", fg="red")
title.pack(pady=20) # وضع العنوان في الأعلى مع مسافة عمودية

# --- Video Frame Placeholder ---
video_frame = Label(window, bg="black", width=720, height=480)
video_frame.pack(pady=10) # وضع الإطار الخاص بالفيديو في المنتصف

# --- Left Side Buttons (Start + Screenshot) ---
left_frame = Frame(window, bg="white") # إطار لتجميع الأزرار في الجهة اليسرى
left_frame.place(x=20, y=150) # تحديد مكانه

btn_start = Button(left_frame, text="Start Video", width=15, font=("Arial", 12),
                    command=lambda: fire_and_body_detection(video_frame, receiver_email))
btn_start.pack(pady=10)

btn_screenshot = Button(left_frame, text="Screenshot", width=15, font=("Arial", 12), command=screenshot)
btn_screenshot.pack(pady=10)

# --- Bottom Center Buttons (End + Exit) ---
bottom_frame = Frame(window, bg="white")
bottom_frame.place(relx=0.5, rely=1.0, anchor='s', y=-40) # يتم وضعه في أسفل النافذة، في الوسط

btn_end = Button(bottom_frame, text="End Video", width=15, font=("Arial", 12), command=end_video)
btn_end.grid(row=0, column=0, padx=20)

btn_exit = Button(bottom_frame, text="Exit Program", width=15, font=("Arial", 12), command=exit_program)
btn_exit.grid(row=0, column=1, padx=20)

# --- Run GUI ---
window.mainloop()
