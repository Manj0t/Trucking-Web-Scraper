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

# Define a job wrapper to pass parameters to the job function
def job_wrapper():
    SL.job(minRPM, maxWeight, origin, end_date, start_date, locations)

# Run job once before scheduling
job_wrapper()
# Schedule the job to run every hour
schedule.every().hour.do(job_wrapper())

while True:
    schedule.run_pending()
    time.sleep(1)