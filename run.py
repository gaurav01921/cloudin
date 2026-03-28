from app.scheduler import start_scheduler
import time

if __name__ == "__main__":
    start_scheduler()

    print("🚀 System started...")

    while True:
        time.sleep(1)
