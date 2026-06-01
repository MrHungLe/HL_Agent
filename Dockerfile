FROM python:3.11-slim

WORKDIR /app

# Sao chép và cài đặt thư viện trước để tận dụng Docker layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn còn lại vào container
COPY . .

EXPOSE 9080

# Chạy app bằng lệnh hypercorn định nghĩa trong main.py
CMD ["python", "main.py"]