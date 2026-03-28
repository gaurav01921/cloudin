from apscheduler.schedulers.background import BackgroundScheduler
from app.collector import collect_metrics
from app.anomaly import detect_anomalies
from app.optimizer import stop_instance


def job():
    print("🔄 Running monitoring cycle...")

    try:
        data = collect_metrics()
        print("📊 Data collected:", data)

        anomalies = detect_anomalies()

        if anomalies:
            print("⚠️ Anomaly detected!")
            stop_instance()
        else:
            print("✅ System normal")

    except Exception as e:
        print("❌ Error:", e)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "interval", seconds=15)
    scheduler.start()
