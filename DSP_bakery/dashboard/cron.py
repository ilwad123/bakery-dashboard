from django_cron import CronJobBase, Schedule
from django.conf import settings
import os
from dashboard.views import sales_data_CNNLTSM
from .cnn_model import predict_from_graph_data
import json
from datetime import timedelta,datetime
class TestCronJob(CronJobBase):
    # schedule = Schedule(run_every_mins=1) used to test if it runs every minute
    schedule = Schedule(run_at_times=['06:00']) # run at 6 AM every Monday
    code = 'test_cron'

    def do(self):
        if datetime.today().weekday() != 0:  
            print("Not Monday ,skipping job.")
            return
        try:
            # Get the sales data from graph database views.py
            df = sales_data_CNNLTSM()

            #gets the models predictions 
            predicted_sales = predict_from_graph_data(df)

            #gets the last date in the dataset
            last_date = df['date'].max()
            #adds 7 days to the last date in the dataset
            next_7_days = [(last_date + timedelta(days=i + 1)).isoformat() for i in range(7)]

            # Convert the predicted sales to a list
            results = {
                "dates": next_7_days,
                "predictions": predicted_sales.tolist()
            }
            # Save the results to a JSON file
            file_path = os.path.join(settings.BASE_DIR, "predicted_sales_cron_output.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)

            print("Model ran and output saved successfully.")
        except Exception as e:
            print("Cron job failed:", e)
        finally:
            #used to test if it does run every week and logs every time it runs
            with open("cron_log.txt", "a") as log:
                log.write(f"{datetime.now().isoformat()} - Ran weekly prediction\n")
