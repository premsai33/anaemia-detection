from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

SCOPES = [
    "https://www.googleapis.com/auth/fitness.heart_rate.read",
    "https://www.googleapis.com/auth/fitness.activity.read"
]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret_566783702683-tgob144mqbefl1h9bjk3imsan7cmer37.apps.googleusercontent.com.json", SCOPES
)

creds = flow.run_local_server(port=0)

service = build("fitness", "v1", credentials=creds)

now = datetime.datetime.utcnow()
start = now - datetime.timedelta(days=1)

dataset_id = f"{int(start.timestamp()*1e9)}-{int(now.timestamp()*1e9)}"

data_source = "derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm"

response = service.users().dataSources().datasets().get(
    userId="me",
    dataSourceId=data_source,
    datasetId=dataset_id
).execute()

points = response.get("point", [])

print("Heart rate data (last 24 hrs):")
for p in points:
    hr = p["value"][0]["fpVal"]
    time = datetime.datetime.fromtimestamp(int(p["startTimeNanos"]) / 1e9)
    print(time, "→", hr)
