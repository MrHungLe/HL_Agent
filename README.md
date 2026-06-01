# 🤖 HL_Agent - AI Customer Service Agent (Restate & Gemini)

Dự án này xây dựng một **AI Agent chăm sóc khách hàng** có khả năng phân tích ý định (Intent) và tự động kích hoạt các công cụ hỗ trợ (Tool Calling) như kiểm tra trạng thái đơn hàng. 

Hệ thống sử dụng **Restate Server** làm bộ điều phối (Orchestrator) giúp đảm bảo các bước xử lý của Agent diễn ra bền bỉ (Durable Execution), tự động sửa sai/thử lại (Retry) khi gặp lỗi mạng hoặc sập nguồn ngầm.

---

## 🛠️ Công Nghệ Sử Dụng

* **Ngôn ngữ chính:** Python 3.11+
* **LLM Brain:** Google Gemini API (`google-genai`)
* **Durable Orchestrator:** [Restate](https://restate.dev/) (Cổng Ingress: `8080`, Cổng Admin: `9070`)
* **Môi trường:** Docker & Docker Compose

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
HL_Agent/
├── docker-compose.yml  # Cấu hình container cho Restate Server và AI Agent
├── Dockerfile          # Đóng gói ứng dụng Python AI Agent vào Docker
├── .env                # Lưu trữ biến môi trường bảo mật (API Key)
├── Makefile            # Lối tắt (Shortcuts) để chạy nhanh các lệnh Terminal
├── requirements.txt    # Danh sách thư viện Python cần cài đặt
├── config.py           # Cấu hình hệ thống và khởi tạo Client
├── tools.py            # Định nghĩa các công cụ của Agent (ví dụ: check_order_status)
├── workflow.py         # Code lõi của Agent (Xử lý chuỗi công việc và kết nối Restate)
├── main.py             # File chạy chính để khởi động Server nội bộ trên cổng 9080
└── chat_cli.py         # Giao diện chat liên tục (Interactive CLI) cho người dùng
```
Bước 1: Cấu hình biến môi trường
Tạo file .env nằm ở thư mục gốc (ngang hàng với docker-compose.yml) và điền API Key lấy từ Google AI Studio:
Đoạn mã
GOOGLE_API_KEY=AIzaSy...your_gemini_api_key...
Bước 2: Khởi động hệ thống với Docker
Chạy lệnh sau để build và kích hoạt các container chạy ngầm:
Bash
docker compose up -d --build
Bước 3: Đăng ký Agent với Restate Server
Mỗi khi khởi động lại Docker mới tinh, bạn cần làm thủ tục để Restate Server nhận diện được Service của AI Agent:
Bash
make register
(Lệnh này sẽ gọi curl đến cổng Admin 9070 của Restate để nạp thông tin service CustomerServiceAgent).
Bước 4: Trải nghiệm Chat với Agent
Để bắt đầu nói chuyện liên tục với Agent ngay trên Terminal giống như ChatGPT, bạn chỉ cần gõ:
Bash
make chat
