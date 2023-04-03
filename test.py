import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET

# Hàm lấy tọa độ các điểm trên bàn tay từ ảnh đầu vào
def get_hand_landmarks(image):
    pass

# Hàm chụp ảnh và lưu tọa độ các điểm trên bàn tay vào file XML
def capture_hand_landmarks(image):
    pass

# Hàm đọc tọa độ các điểm từ file XML
def read_hand_landmarks_from_xml(xml_file):
    pass

# Hàm lưu tọa độ các điểm vào file XML
def save_hand_landmarks_to_xml(landmarks):
    pass

# Hàm kiểm tra xem tọa độ các điểm trong hai danh sách landmarks1 và landmarks2 có giống nhau ít nhất 80% không
def check_matching_landmarks(landmarks1, landmarks2):
    pass

# Hàm lấy danh sách tên các file XML trong thư mục
def get_xml_files_in_folder():
    pass

# Khởi tạo camera
cap = cv2.VideoCapture(0)
# Kiểm tra xem camera đã mở hay chưa
if not cap.isOpened():
    raise IOError("Không thể mở camera")

# Tạo cửa sổ để hiển thị hình ảnh
cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)


def read_hand_landmarks_from_xml(xml_file):
    """
    Đọc tọa độ các điểm trên bàn tay từ file XML.
    """
    landmarks = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for point in root.findall("./hand/point"):
        id = int(point.get("id"))
        x = int(point.get("x"))
        y = int(point.get("y"))
        landmarks.append((id, x, y))
    return landmarks


def save_hand_landmarks_to_xml(landmarks, xml_file=None):
    """
    Lưu tọa độ các điểm trên bàn tay vào file XML.
    """
    if xml_file is None:
        # Tạo tên file mới dựa trên thời gian hiện tại
        xml_file = f"hand_landmarks_{int(time.time())}.xml"
    root = ET.Element("hand")
    for landmark in landmarks:
        point = ET.SubElement(root, "point", {"id": str(landmark[0]), "x": str(landmark[1]), "y": str(landmark[2])})
    tree = ET.ElementTree(root)
    tree.write(xml_file)
    return xml_file


def start_camera():
    """
    Khởi động camera và cho phép người dùng chụp ảnh và ghi chú.
    """
    # Khởi tạo camera
    cap = cv2.VideoCapture(0)
    # Kiểm tra xem camera đã mở hay chưa
    if not cap.isOpened():
        raise IOError("Không thể mở camera")

    # Tạo cửa sổ để hiển thị hình ảnh
    cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

    while True:
        # Đọc một khung hình từ camera
        ret, khung_anh = cap.read()
        # Lật khung hình
        khung_anh = cv2.flip(khung_anh, 1)

        # Thay đổi kích thước hình ảnh để giữ nguyên tỷ lệ khung hình
        ratio = 1.5
        khung_anh = cv2.resize(khung_anh, (int(khung_anh.shape[1] * ratio), int(khung_anh.shape[0] * ratio)))

        # Hiển thị khung hình trên cửa sổ
        cv2.imshow('Webcam', khung_anh)

        # Nếu người dùng nhấn phím ESC hoặc đóng cửa sổ, thoát khỏi chương trình
        key = cv2.waitKey(1)
        if key == 27 or cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE) < 1:
            break

        # Nếu người dùng nhấn nút "Chụp ảnh"
        if key == ord('c'):
            # Chụp ảnh và lưu tọa độ các điểm trên bàn tay vào một file XML mới
            landmarks = get_hand_landmarks(khung_anh)
            xml_file = save_hand_landmarks_to_xml(landmarks)

            # Hiển thị cửa sổ ghi chú để người dùng nhập nội dung ghi chú
            g
