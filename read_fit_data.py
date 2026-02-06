from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

# Google Fit scopes
SCOPES = [
    "https://www.googleapis.com/auth/fitness.activity.read"
]

# OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret_195894763934-vq77nth3vso8btd77jptp70j2kdoug89.apps.googleusercontent.com.json",  # CHANGE THIS to your actual filename
    SCOPES
)

creds = flow.run_local_server(port=0)

service = build("fitness", "v1", credentials=creds)

# Time range: last 24 hours
now = datetime.datetime.utcnow()
start = now - datetime.timedelta(days=1)

dataset_id = f"{int(start.timestamp()*1e9)}-{int(now.timestamp()*1e9)}"

# Step count data source
data_source = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"

response = service.users().dataSources().datasets().get(
    userId="me",
    dataSourceId=data_source,
    datasetId=dataset_id
).execute()

points = response.get("point", [])

print("Steps data (last 24 hours):")
for p in points:
    steps = p["value"][0]["intVal"]
    time = datetime.datetime.fromtimestamp(int(p["startTimeNanos"]) / 1e9)
    print(time, "→", steps)

import pandas as pd
import os

# Prepare data list
records = []

for p in points:
    steps = p["value"][0]["intVal"]
    time = datetime.datetime.fromtimestamp(int(p["startTimeNanos"]) / 1e9)
    records.append([str(time), steps])

# Convert to DataFrame
df = pd.DataFrame(records, columns=["timestamp", "steps"])

# Create folder if not exists
os.makedirs("daily_logs", exist_ok=True)

# Create filename for today
filename = f"daily_logs/steps_{now.date()}.csv"

# Save file
df.to_csv(filename, index=False)

print(f"Saved today's steps to: {filename}")
