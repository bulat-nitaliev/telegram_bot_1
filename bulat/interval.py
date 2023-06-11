from schedule import every, repeat, run_pending
import time

# Обновляем for beginner один раз в неделю в 12:00
@repeat(every().week.at("12.00"))
def job():
    print("I am a scheduled job")

while True:
    run_pending()
    time.sleep(1)