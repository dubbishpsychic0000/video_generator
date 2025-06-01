import schedule
import time
from main import run_full_pipeline
import config

def schedule_daily_upload():
    """Schedule daily video uploads"""
    topics = [
        "Why bridges have expansion joints",
        "How skyscrapers stay upright in wind",
        "The engineering behind tunnels",
        "Why roads crack in winter",
        "How elevators work safely"
    ]
    
    topic_index = 0
    
    def run_scheduled():
        nonlocal topic_index
        topic = topics[topic_index % len(topics)]
        print(f"Running scheduled upload for topic: {topic}")
        run_full_pipeline(topic)
        topic_index += 1
    
    # Schedule for 10 AM daily
    schedule.every().day.at("10:00").do(run_scheduled)
    
    print("Scheduler started. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("Scheduler stopped.")

if __name__ == "__main__":
    schedule_daily_upload()
