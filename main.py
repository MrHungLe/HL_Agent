import restate
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from config import PORT
from workflow import customer_service # Chỉ import biến service này thôi

# Đăng ký biến customer_service vào Restate App
app = restate.app(services=[customer_service])

# Chạy thông qua Hypercorn khi file được gọi trực tiếp
if __name__ == "__main__":
    config = Config()
    # 0.0.0.0 rất quan trọng để Docker có thể expose port ra ngoài
    config.bind = [f"0.0.0.0:{PORT}"]
    
    print(f"Agent Service đang chạy tại port {PORT}...")
    asyncio.run(serve(app, config))