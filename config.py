import os

# Cấu hình API và Port
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
PORT = int(os.getenv("PORT", "9080"))

# Kiểm tra nếu chưa cấu hình API Key
if not GOOGLE_API_KEY:
    print("CẢNH BÁO: Chưa cấu hình GOOGLE_API_KEY trong biến môi trường!")