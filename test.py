import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import threading


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Camera App")
        self.cap = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()
        self.btn_capture = tk.Button(self.window, text="Chụp ảnh", command=self.capture_image)
        self.btn_capture.pack(side="bottom", pady=10)
        self.image = None

    def show_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(20, self.show_video)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            self.image = frame
            t = threading.Thread(target=self.save_image)
            t.start()

    def save_image(self):
        if not os.path.exists("images"):
            os.makedirs("images")
        filename = os.path.join("images", "image.jpg")
        cv2.imwrite(filename, self.image)
        print("Đã chụp ảnh và lưu vào", filename)

    def run(self):
        self.show_video()
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

    # Kiểm tra xem đã có folder "images" chưa, nếu chưa có thì tạo
    if not os.path.exists("images"):
        os.makedirs("images")
    
    # Thêm button "Chụp ảnh" vào giao diện
    btn_capture = tk.Button(app.window, text="Chụp ảnh", command=app.capture_image)
    btn_capture.pack(side="bottom", pady=10)
    
    # Thực thi vòng lặp chính của ứng dụng
    app.window.mainloop()