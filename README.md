# LẬP TRÌNH PYTHON VỚI GIAO THỨC CoAP

1. THÔNG TIN SINH VIÊN
- Nguyễn Tiến Anh – B23DCCN037
- Nguyễn Văn Quang – B23DCCN690

2. PHIÊN BẢN PYTHON VÀ CÁC THƯ VIỆN SỬ DỤNG
- Python: Phiên bản 3.x (Khuyến nghị Python 3.8+)
- Thư viện chính: aiocoap (Hỗ trợ xây dựng CoAP Server, Client và cơ chế Observe)
- Lệnh cài đặt thư viện: pip install aiocoap

3. CÁCH CÀI ĐẶT MÔI TRƯỜNG
- Bước 1: Đảm bảo đã cài đặt Python 3.x trên hệ thống.
- Bước 2: Mở terminal/cmd và cài đặt thư viện bằng lệnh:
  pip install aiocoap
- Lưu ý mạng: Giao thức CoAP chạy trên UDP, cổng mặc định là 5683. Khi chạy trên hai máy khác nhau, cần cho phép tường lửa (Firewall) mở cổng UDP 5683.

4. CẤU TRÚC THƯ MỤC
```text
   CoAP_Lab/
|
|-- bai1/
|   |-- coap_server_bai1.py
|   |-- coap_client_bai1.py
|
|-- bai2/
|   |-- sensor_server_bai2.py
|   |-- monitor_client_bai2.py
|
|-- bai3/
|   |-- light_server_bai3.py
|   |-- light_controller_bai3.py
|   |-- light_monitor_bai3.py
|
|-- README.md
```
5. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH

BÀI 1: Giao tiếp CoAP cơ bản (GET & POST) 
- Terminal 1 (Khởi động Server):
  python bai1/coap_server_bai1.py
- Terminal 2 (Chạy Client gửi yêu cầu):
  python bai1/coap_client_bai1.py

BÀI 2: Mô phỏng cảm biến nhiệt độ & độ ẩm 
- Terminal 1 (Khởi động Sensor Server):
  python bai2/sensor_server_bai2.py
- Terminal 2 (Khởi động Monitoring Client):
  python bai2/monitor_client_bai2.py

BÀI 3: Hệ thống đèn thông minh với CoAP Observe
(Cần mở đồng thời 3 terminal riêng biệt)
- Terminal 1 (Khởi động Smart Light Server):
  python bai3/light_server_bai3.py
- Terminal 2 (Khởi động Monitoring Client theo dõi thời gian thực):
  python bai3/light_monitor_bai3.py
- Terminal 3 (Khởi động Controller Client điều khiển):
  python bai3/light_controller_bai3.py
  (Nhập trực tiếp các lệnh từ bàn phím: ON, OFF, STATUS, EXIT)

6. ĐỊA CHỈ IP, CỔNG VÀ URI CÁC TÀI NGUYÊN CoAP
- Host/IP chạy cục bộ: 127.0.0.1 (localhost)
- Cổng mặc định: 5683
- Danh sách URI tài nguyên:
  + Bài 1: coap://localhost:5683/iot/lab/message (GET, POST)
  + Bài 2: coap://localhost:5683/iot/lab/sensor01/data (GET định kỳ 3s)
  + Bài 3: coap://localhost:5683/iot/lab/light01/status (GET, PUT, OBSERVE)

7. KẾT QUẢ ĐẠT ĐƯỢC VÀ LOG MINH CHỨNG

- Bài 1:
+ Testcase 1:

 Client
 ```text
  Sending GET request...
  Response:
  Code: 2.05 Content
  Payload: Xin chao tu CoAP Server

  Sending POST request...
  Payload: Xin chao tu CoAP Client - B23DCCN037 - Nguyen Tien Anh

  Response:
  Code: 2.04 Changed
  Payload: Server da nhan thong diep
```
Server
```text  
  POST request received:
  Payload: Xin chao tu CoAP Client - B23DCCN037 - Nguyen Tien Anh
  Time: 07:45:28
```
Testcase 2:

Client
```text  
  Sending GET request...
  Response:
  Code: 2.05 Content
  Payload: Xin chao tu CoAP Server

  Sending POST request...
  Payload: Xin chao tu CoAP Client - B23DCCN690 - Nguyen Van Quang

  Response:
  Code: 2.04 Changed
  Payload: Server da nhan thong diep
```
Server
```text
  POST request received:
  Payload: Xin chao tu CoAP Client - B23DCCN690 - Nguyen Van Quang
  Time: 07:47:56
```
- Bài 2:
```text
  [15:27:41] Received sensor data
  Device: sensor01
  Temperature: 26.3 C
  Humidity: 50.4 %
  Trang thai: Binh thuong
  ----------------------------------

  [15:27:44] Received sensor data
  Device: sensor01
  Temperature: 30.0 C
  Humidity: 88.9 %
  Trang thai: Binh thuong
  ----------------------------------
  [15:27:47] Received sensor data
  Device: sensor01
  Temperature: 27.7 C
  Humidity: 36.2 %
  CANH BAO: Do am thap
  ----------------------------------
  [15:27:50] Received sensor data
  Device: sensor01
  Temperature: 30.8 C
  Humidity: 52.2 %
  Trang thai: Binh thuong
  ----------------------------------
```
- Bài 3:

Controller
 ```text
  Nhap lenh: ON
  Sending PUT request...
  Response Code: 2.04 Changed
  Da bat den light01

  Nhap lenh: OFF
  Sending PUT request...
  Response Code: 2.04 Changed
  Da tat den light01

  Nhap lenh: STATUS
  Sending GET request...
  Response: {"device_id": "light01", "status": "OFF"}

  Nhap lenh: ee
  Lenh khong hop le.

  Nhap lenh: EXIT
  Exiting controller...
 ```
Server
```text
  CoAP Smart Light Server started...
  Resource: /iot/lab/light01/status

  GET request received
  PUT request received:
  Device: light01
  Command: ON
  Light state changed: OFF -> ON
  Notify observers: ON

  GET request received
  PUT request received:
  Device: light01
  Command: OFF
  Light state changed: ON -> OFF
  Notify observers: OFF

  GET request received
  GET request received
```
Monitor
```text  
  Registering CoAP Observe...

  [15:31:06] State Update Received
  Device: light01
  Status: ON

  [15:31:09] State Update Received
  Device: light01
  Status: OFF
