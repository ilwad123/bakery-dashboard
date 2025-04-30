from django_cron import CronJobBase, Schedule
from django.conf import settings
import os
import json
from datetime import timedelta, datetime
from neo4j.exceptions import ServiceUnavailable
from dashboard.views import sales_data_CNNLTSM
from .cnn_model import predict_from_graph_data

class TestCronJob(CronJobBase):
    schedule = Schedule(run_every_mins=5)
    code = 'test_cron'

    def do(self):
        # Only run on Wednesday 
        if datetime.today().weekday() != 2:  # 2 is Wednesday
            print("Not Wednesday, skipping job.")
            return

        # Path to the log file
        log_path = os.path.join(settings.BASE_DIR, "cron_log.txt")
        today_str = datetime.now().strftime('%Y-%m-%d')


        # Skip if already ran today 
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                if today_str in f.read():
                    print("Prediction already run today, skipping.")
                    return


        try:
            try:
                # Attempt to connect to the database
                # Get the sales data from graph database views.py
                df = sales_data_CNNLTSM()
            except ServiceUnavailable as e:
                # Handle the case where Neo4j is not available
                print("Neo4j not available, skipping this run. Will retry.")
                return

            # Gets the model's predictions
            predicted_sales = predict_from_graph_data(df)

            # Gets the last date in the dataset
            last_date = df['date'].max()
            # Adds 7 days to the last date in the dataset
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

            print("Model ran and output saved successfully")

            # Log successful run 
            with open(log_path, "a") as log:
                log.write(f"{datetime.now().isoformat()} - Ran weekly prediction\n")

        except Exception as e:
            print("Cron job failed:", e)
