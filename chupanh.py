import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import os
import pickle


# --------------------- Phần xử lý nhận diện bàn tay và hiển thị lên camera ---------------------
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


# --------------------- Phần lưu file dữ liệu nhận diện bàn tay ---------------------
def save_hand_landmarks():
    img = capture_and_process()
    save_path = "hello.xml"

    if os.path.exists(save_path):
        with open(save_path, "a") as f:
            anh_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ket_qua = tay.process(anh_rgb)
            if ket_qua.multi_hand_landmarks:
                for hand_landmarks in ket_qua.multi_hand_landmarks:
                    f.write(str(hand_landmarks))
                    f.write("\n")
    else:
        with open(save_path, "w") as f:
            anh_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ket_qua = tay.process(anh_rgb)
            if ket_qua.multi_hand_landmarks:
                for hand_landmarks in ket_qua.multi_hand_landmarks:
                    f.write(str(hand_landmarks))
                    f.write("\n")

    print(f"Đã lưu dữ liệu vào file: {save_path}")


# --------------------- Phần đọc file dữ liệu và hiển thị lên màn hình ---------------------
# --------------------- Phần đọc file dữ liệu và hiển thị lên màn hình ---------------------
def read_and_display_data():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if not file_path:
        return
    with open(file_path, "r") as f:
        data = f.read()
    hand_landmarks = []
    for line in data.splitlines():
        if line.startswith("x") or line.startswith("y") or line.startswith("z"):
            continue
        landmark = line.strip().split(" ")
        landmark = [float(val) for val in landmark]
        hand_landmarks.append(landmark)

    # Hiển thị tên file XML lên màn hình
    file_name_label.config(text=f"File: {os.path.basename(file_path)}")

    # Vẽ khoảng vùng bàn tay trên camera
    while True:
        ret, khung_anh = cap.read()
        if not ret:
            break
        khung_anh = cv2.flip(khung_anh, 1)
        for landmark in hand_landmarks:
            x, y = int(landmark[1] * khung_anh.shape[1]), int(landmark[2] * khung_anh.shape[0])
            cv2.circle(khung_anh, (x, y), 5, (0, 255, 0), -1)

        img = cv2.cvtColor(khung_anh, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        image_label.config(image=img)
        image_label.image = img
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    # Tạo button để chọn file XML và hiển thị dữ liệu trên camera
select_file_button = tk.Button(window, text="Chọn file XML", command=read_and_display_data)
select_file_button.pack()


# --------------------- Phần lưu file dữ liệu nhận diện bàn tay ---------------------
def read_and_display_data():
    if not data_files:
        return

    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        # Chạy phần đọc file dữ liệu trong một thread mới
        threading.Thread(target=read_data_file, args=(file_path,), daemon=True).start()

# Hàm đọc dữ liệu từ file và hiển thị trên camera
def read_data_file(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    hand_landmarks = []
    for line in data.splitlines():
        if line.startswith("x") or line.startswith("y") or line.startswith("z"):
            continue
        landmark = line.strip().split(" ")
        landmark = [float(val) for val in landmark]
        hand_landmarks.append(landmark)

    # Hiển thị tên file XML lên màn hình
    file_name_label.config(text=f"File: {os.path.basename(file_path)}")

    # Vẽ khoảng vùng bàn tay trên camera
    while True:
        ret, khung_anh = cap.read()
        if not ret:
            break
        khung_anh = cv2.flip(khung_anh, 1)
        for landmark in hand_landmarks:
            x, y = int(landmark[1] * khung_anh.shape[1]), int(landmark[2] * khung_anh.shape[0])
            cv2.circle(khung_anh, (x, y), 5, (0, 255, 0), -1)

        img = cv2.cvtColor(khung_anh, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        image_label.config(image=img)
        image_label.image = img
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
# --------------------- Tạo giao diện ---------------------
window = tk.Tk()
window.title("Hand Tracking")

# Tạo label để hiển thị ảnh từ camera
image_label = tk.Label(window)
image_label.pack()

# Tạo button để chụp ảnh
capture_button = tk.Button(window, text="Chụp", command=lambda: threading.Thread(target=save_hand_landmarks).start())
capture_button.pack()

# Tạo label để hiển thị tên file
file_name_label = tk.Label(window, text="")
file_name_label.pack()

# Tạo button để đọc dữ liệu từ file đã lưu
read_data_button = tk.Button(window, text="Đọc dữ liệu", command=read_and_display_data)
read_data_button.pack()

# Khởi chạy phần update hình ảnh từ camera
window.after(10, update_image_label)
window.mainloop()

cap.release()
