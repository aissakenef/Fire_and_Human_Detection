import cv2 as cv
import pyautogui
from datetime import datetime
import smtplib
import threading
from tkinter import messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO


# Globals
cap = None
streaming = False
video_frame_ref = None

# --- Fire and Human Detection ---
def fire_and_body_detection(video_frame, receiver_email):
    global cap, streaming, video_frame_ref
    url = "http://192.168.8.100:5000/video_feed"
    cap = cv.VideoCapture("http://192.168.8.100:5000/video_feed") # start stream from camera
    if not cap.isOpened(): # if don't open camera
        messagebox.showwarning(title='Warning', message='Failed to open the camera.') # display message error 
        return
    model_fire = YOLO('fire.pt')   # Model for fire
    model_human = YOLO('human.pt')  # Model for human

    video_frame_ref = video_frame
    streaming = True

    def update(): # عرض الفيديو بشكل مستمر 
        global streaming
        if not streaming:
            return

        ret, frame = cap.read()  # التقاط صورة من الكاميرا
        if not ret:
            return

        # تشغيل الكشف على الصورة باستخدام النموذجين
        results_fire = model_fire(frame)[0]
        results_human = model_human(frame)[0]

        annotated_frame = frame.copy() # تشغيل الكشف على الصورة باستخدام النموذجين
        
        # تهيئة متغيرات منطقية لتحديد هل يجب إرسال تنبيه بالبريد أو لا.
        fire_detected = False
        human_detected = False

        # Fire detections
        for box in results_fire.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            if conf > 0.5: #إذا كانت  أكثر من 50%، نعتبر أن الكشف موثوق
                fire_detected = True
                cv.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv.putText(annotated_frame, "FIRE", (x1, y1 - 10),
                            cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Human detections
        for box in results_human.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            if conf > 0.5 and cls_id == 0:  # class 0 = person
                human_detected = True
                cv.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv.putText(annotated_frame, "PERSON", (x1, y1 - 10),
                            cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # يبعت ايميل مرة واحدة
        if (fire_detected or human_detected) and not update.run_once:
            threading.Thread(target=send_email, args=(receiver_email,)).start()
            update.run_once = True

        # Resize for GUI display
        frame_rgb = cv.resize(annotated_frame, (720, 480))
        frame_rgb = cv.cvtColor(frame_rgb, cv.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

        video_frame.config(image=img) # عرض الصورة في واجهة المستخدم
        video_frame.image = img # يحفظ الصورة داخل العنصر لمنع حذفها تلقائيًا.

        video_frame.after(10, update) # تكرار التحديث كل 10 ميلي ثانية

    update.run_once = False
    update()

# --- End Video ---
def end_video():
    global cap, streaming, video_frame_ref
    streaming = False # إيقاف البث
    if cap:
        cap.release() # تحرير الكاميرا
        cap = None
    cv.destroyAllWindows() # إغلاق نوافذ OpenCV

    # Show black background in the video_frame
    if video_frame_ref:
        from PIL import Image, ImageTk
        black_image = Image.new('RGB', (720, 480), 'black')
        img = ImageTk.PhotoImage(black_image)
        video_frame_ref.config(image=img)
        video_frame_ref.image = img

# --- Screenshot ---
def screenshot():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') # توقيت الصورة
    screenshot = pyautogui.screenshot() # التقاط الشاشة
    screenshot.save(f'image_{timestamp}.png') # حفظها باسم

# --- Send Email Alert ---
def send_email(receiver_email):
    sender = "ssaai2031@gmail.com"
    password = "hahp mekv ddzg rnoi"
    subject = "Warning!"
    body = "Something Detected"

    message = f"""From: {sender}
To: {receiver_email}
Subject: {subject}

{body}
"""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls() # تشفير الاتصال
    try:
        server.login(sender, password) # تسجيل الدخول
        server.sendmail(sender, receiver_email, message) # إرسال الرسالة
    except smtplib.SMTPAuthenticationError:
        messagebox.showwarning(title="Warning", message="Unable to LogIn!") # afficher message
