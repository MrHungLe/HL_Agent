import restate
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from config import PORT
from workflow import customer_service 

app = restate.app(services=[customer_service])

if __name__ == "__main__":
    config = Config()
    config.bind = [f"0.0.0.0:{PORT}"]
    
    print(f"Agent Service đang chạy tại port {PORT}...")
    asyncio.run(serve(app, config))