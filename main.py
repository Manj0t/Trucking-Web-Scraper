import scrapingLogic as SL
import schedule
import time
import json
import sys

# Data is passed in from runner.py
data = sys.argv[1]
locations = json.loads(data)

minRPM = float(locations.pop(0))
maxWeight = float(locations.pop(0))
origin = locations.pop(0)
start_date = locations.pop(0)
end_date = locations.pop(0)

# Run job once before scheduling
SL.job(minRPM, maxWeight, origin, end_date, start_date, locations)

# Schedule the job to run every hour
schedule.every().hour.do(SL.job(minRPM, maxWeight, origin, end_date, start_date, locations))

while True:
    schedule.run_pending()
    time.sleep(1)