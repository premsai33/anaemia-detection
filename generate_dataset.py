import pandas as pd
import random

data = []

for _ in range(100):
    heart_rate = random.randint(65, 110)
    steps = random.randint(2000, 10000)
    sleep_hours = round(random.uniform(4.5, 8.5), 1)

    # Rule-based anemia labeling (indirect)
    if heart_rate > 90 and steps < 5000 and sleep_hours < 6:
        anaemia = 1
    else:
        anaemia = 0

    data.append([heart_rate, steps, sleep_hours, anaemia])

df = pd.DataFrame(
    data,
    columns=["heart_rate", "steps", "sleep_hours", "anaemia"]
)

df.to_csv("data/wearable_anemia_dataset.csv", index=False)

print("Dataset generated successfully with", len(df), "rows")
