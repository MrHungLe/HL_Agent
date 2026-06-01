import requests
import json

URL = "http://localhost:8080/CustomerServiceAgent/process_chat"
HEADERS = {"Content-Type": "application/json"}

print("🤖 Đã kết nối với AI Agent! (Gõ 'exit' hoặc 'quit' để thoát)")
print("-" * 50)

while True:
    try:
        # 1. Chờ người dùng nhập tin nhắn
        user_input = input("Bạn: ")
        
        # 2. Kiểm tra nếu muốn thoát
        if user_input.lower() in ['exit', 'quit']:
            print("Tạm biệt!")
            break
        if not user_input.strip():
            continue

        # 3. Gửi tin nhắn đến Agent qua Restate
        # Dùng tham số json=user_input để thư viện tự động bọc chuỗi vào cặp ngoặc kép thành JSON String
        response = requests.post(URL, headers=HEADERS, json=user_input)

        # 4. In câu trả lời
        if response.status_code == 200:
            print(f"Agent: {response.json()}")
        else:
            print(f"[Lỗi Server {response.status_code}]: {response.text}")

    except KeyboardInterrupt:
        print("\nTạm biệt!")
        break
    except requests.exceptions.ConnectionError:
        print("\n[Lỗi kết nối]: Không thể gọi đến localhost:8080. Bạn đã chạy Docker chưa?")
        break