import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading

mp_duyet_tay = mp.solutions.hands
mp_ghi_chu = mp.solutions.drawing_utils

# Khởi tạo đối tượng Hand để nhận diện bàn tay
tay = mp_duyet_tay.Hands(static_image_mode=False,
                         max_num_hands=2,
                         min_detection_confidence=0.5,
                         min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

def capture_and_process():
    ret, khung_anh = cap.read()
    khung_anh = cv2.flip(khung_anh, 1)
    anh_rgb = cv2.cvtColor(khung_anh, cv2.COLOR_BGR2RGB)
    ket_qua = tay.process(anh_rgb)

    if ket_qua.multi_hand_landmarks:
        for diem_dac_trung in ket_qua.multi_hand_landmarks:
            mp_ghi_chu.draw_landmarks(khung_anh, diem_dac_trung, mp_duyet_tay.HAND_CONNECTIONS)
    
    return khung_anh

def update_image_label():
    img = capture_and_process()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    image_label.config(image=img)
    image_label.image = img
    window.after(10, update_image_label)

def save_hand_landmarks():
    img = capture_and_process()
    save_path = filedialog.asksaveasfilename(defaultextension=".xml")

    if save_path:
        with open(save_path, "w") as f:
            anh_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ket_qua = tay.process(anh_rgb)
            if ket_qua.multi_hand_landmarks:
                for hand_landmarks in ket_qua.multi_hand_landmarks:
                    f.write(str(hand_landmarks))
                    f.write("\n")

window = tk.Tk()
window.title("Hand Tracking")

image_label = tk.Label(window)
image_label.pack()

capture_button = tk.Button(window, text="Chụp", command=lambda: threading.Thread(target=save_hand_landmarks).start())
capture_button.pack()

window.after(10, update_image_label)
window.mainloop()

cap.release()
