import asyncio
from datetime import datetime
from app.services.daily_scanner import run_daily_scan


async def daily_scan_task():
    print(f"[{datetime.now()}] Starting daily scan...")
    try:
        result = await run_daily_scan()
        print(f"[{datetime.now()}] Scan complete: {result['total_found']} laws found")
        print(f"  Sources: {result['sources']}")
    except Exception as e:
        print(f"[{datetime.now()}] Scan failed: {e}")


def start_scheduler():
    try:
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        scheduler = AsyncIOScheduler()
        scheduler.add_job(daily_scan_task, 'cron', hour=2, minute=0, id='daily_scan')
        scheduler.start()
        print("Scheduler started: daily scan at 2:00 AM PKT")
        return scheduler
    except ImportError:
        print("APScheduler not installed. Daily scan disabled.")
        return None
