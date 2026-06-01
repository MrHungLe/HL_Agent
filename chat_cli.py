import requests
import json

URL = "http://localhost:8080/CustomerServiceAgent/process_chat"
HEADERS = {"Content-Type": "application/json"}

print("🤖 Đã kết nối với AI Agent! (Gõ 'exit' hoặc 'quit' để thoát)")
print("-" * 50)

while True:
    try:
        user_input = input("Bạn: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Tạm biệt!")
            break
        if not user_input.strip():
            continue
        response = requests.post(URL, headers=HEADERS, json=user_input)

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