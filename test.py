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
            landmarks = capture_hand_landmarks(khung_anh)
            xml_file = save_hand_landmarks_to_xml(landmarks)

            # Hiển thị cửa sổ ghi chú để người dùng nhập nội dung ghi chú
            ghi_chu = input("Nhập ghi chú: ")

            # Lưu ghi chú vào file XML
            tree = ET.parse(xml_file)
            root = tree.getroot()
            note_element = ET.SubElement(root, "note")
            note_element.text = ghi_chu
            tree.write(xml_file)
        
        # Nếu người dùng nhấn nút "Đọc dữ liệu"
        if key == ord('r'):
            # Lấy tọa độ các điểm trên bàn tay của camera
            landmarks = get_hand_landmarks(khung_anh)
            # Lấy danh sách tên các file xml trong thư mục
            xml_files = get_xml_files_in_folder()
            # Duyệt qua từng file xml và so sánh tọa độ điểm trên camera với tọa độ điểm trong file xml
            for xml_file in xml_files:
                file_landmarks = read_hand_landmarks_from_xml(xml_file)
                match = check_landmarks_match(file_landmarks, landmarks)
                # Nếu trùng khớp tọa độ điểm trên camera với tọa độ điểm trong file xml ít nhất 80%, hiển thị tên file và ghi chú lên màn hình chính
                if match:
                    print(f"{xml_file}: {match['note']}")
                    cv2.putText(khung_anh, f"{xml_file}: {match['note']}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            # Hiển thị khung hình trên cửa sổ
            cv2.imshow('Webcam', khung_anh)
# Hiển thị hình ảnh và chờ đợi người dùng tắt chương trình
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

    # Nếu người dùng đóng cửa sổ hoặc nhấn phím ESC, thoát khỏi chương trình
    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE) < 1:
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
# Lưu ảnh kết quả
now = datetime.now()
img_name = now.strftime("%Y-%m-%d_%H-%M-%S.jpg")
cv2.imwrite(img_name, khung_anh)

# Lưu lại các tọa độ điểm vào file XML
def save_hand_landmarks_to_xml(landmarks):
    # Tạo phần tử gốc có tên "hand_landmarks"
    root = ET.Element("hand_landmarks")

    # Thêm các phần tử con cho từng điểm trên bàn tay
    for i, point in enumerate(landmarks):
        point_element = ET.SubElement(root, "point", id=str(i), x=str(point[0]), y=str(point[1]))

    # Ghi nội dung của phần tử gốc vào file XML
    xml_file_name = "hand_landmarks.xml"
    tree = ET.ElementTree(root)
    tree.write(xml_file_name)

    return xml_file_name
# Nếu người dùng nhấn nút "Xóa dữ liệu"
if key == ord('x'):
    # Lấy danh sách tên các file xml trong thư mục
    xml_files = get_xml_files_in_folder()
    if xml_files:
        # Hiển thị danh sách các file xml và cho phép người dùng chọn file cần xóa
        print("Chọn file để xóa:")
        for i, xml_file in enumerate(xml_files):
            print(f"{i+1}. {xml_file}")
        selected_index = int(input("> ")) - 1
        selected_file = xml_files[selected_index]
        # Xóa bỏ file đã chọn
        os.remove(selected_file)
        print(f"Đã xóa file {selected_file}")
    else:
        print("Không có file để xóa.")

