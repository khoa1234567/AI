import cv2
import xml.etree.ElementTree as ET
import os


# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Lấy đường dẫn thư mục hiện tại
folder_path = os.getcwd()

# Lấy danh sách tất cả các file trong thư mục
all_files = os.listdir(folder_path)
# Lọc ra các file có đuôi ".xml" và lưu vào danh sách "xml_files"
xml_files = [f for f in all_files if f.endswith('.xml')]

# Tạo cửa sổ để hiển thị hình ảnh
cv2.namedWindow("Webcam")

# Thực hiện vòng lặp để đọc dữ liệu từ camera và hiển thị lên màn hình
while True:
    # Đọc khung hình từ camera
    ret, khung_anh = cap.read()

    # Lật khung hình
    khung_anh = cv2.flip(khung_anh, 1)

    # Thay đổi kích thước hình ảnh để giữ nguyên tỷ lệ khung hình
    ratio = 1
    khung_anh = cv2.resize(khung_anh, (int(khung_anh.shape[1] * ratio), int(khung_anh.shape[0] * ratio)))

    # Hiển thị hình ảnh lên khung hình
    cv2.imshow("Webcam", khung_anh)

    # Đọc tọa độ các điểm từ file XML và so sánh với tọa độ trên camera
    for xml_file in xml_files:
        landmarks = read_hand_landmarks_from_xml(xml_file)
        if match_hand_landmarks(landmarks, hand_landmarks):
            print(f"Tên file: {xml_file} (có tọa độ giống tay trên màn hình ít nhất 80%)")
            cv2.putText(khung_anh, xml_file, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    # Chờ và kiểm tra phím ESC hoặc nút X được nhấn để thoát
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or cv2.getWindowProperty('Webcam', cv2.WND_PROP_VISIBLE) < 1:
        break

# Giải phóng tài nguyên liên quan và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()

# nút chụp
def capture_hand_landmarks(self):
    # Chụp ảnh
    ret, frame = self.cap.read()

    # Kiểm tra nếu không thể chụp ảnh
    if not ret:
        self.display_error("Không thể chụp được tọa độ các điểm trên bàn tay!")
        return

    # Lật khung hình
    frame = cv2.flip(frame, 1)

    # Thay đổi kích thước hình ảnh để giữ nguyên tỷ lệ khung hình
    ratio = self.frame_width / frame.shape[1]
    frame_resized = cv2.resize(frame, (int(frame.shape[1] * ratio), int(frame.shape[0] * ratio)))

    # Hiển thị hình ảnh lên khung hình
    self.update_image(frame_resized)

    # Lưu tọa độ các điểm trên bàn tay vào file XML mới
    root = ET.Element("hand_landmarks")

    # Tạo các phần tử cho các điểm trên bàn tay
    for lm in self.hand_landmarks:
        point_element = ET.SubElement(root, "point")
        point_element.set("id", str(lm.id))
        point_element.set("x", str(lm.x))
        point_element.set("y", str(lm.y))

    # Hiển thị cửa sổ ghi chú để người dùng nhập nội dung ghi chú
    note_text = ""
    while True:
        # Hiển thị hình ảnh và cửa sổ ghi chú
        self.update_image(frame_resized)
        note_text = self.display_note_window()

        # Nếu người dùng nhấn nút "Lưu" thì lưu ghi chú và tọa độ điểm trên bàn tay vào file XML
        if self.note_window.saved:
            # Thêm phần tử ghi chú vào file XML
            note_element = ET.SubElement(root, "note")
            note_element.text = note_text

            # Lưu file XML
            tree = ET.ElementTree(root)
            filename = "hand_landmarks_" + str(uuid.uuid4()) + ".xml"
            tree.write(filename)
            print(f"Đã lưu tọa độ điểm trên bàn tay vào file {filename}")
            break

        # Nếu người dùng nhấn nút "Hủy" thì thoát khỏi cửa sổ ghi chú và không lưu file XML
        elif self.note_window.canceled:
            break
# nút đọc dữ liệu

def read_hand_landmarks_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    landmarks = []
    for point in root.findall(".//point"):
        x = int(point.get("x"))
        y = int(point.get("y"))
        landmarks.append((x, y))
    return landmarks
