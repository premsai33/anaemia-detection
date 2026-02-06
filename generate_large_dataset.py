import pandas as pd
import random

rows = 5000
data = []

for _ in range(rows):

    age = random.randint(18, 65)

    gender = random.choice(["Male", "Female"])

    sleep_hours = round(random.uniform(4.0, 9.0), 1)

    heart_rate = random.randint(55, 115)

    spo2 = random.randint(88, 100)

    steps = random.randint(1500, 15000)

    # Improved anemia risk logic
    risk_score = 0

    if heart_rate > 95:
        risk_score += 1
    if spo2 < 94:
        risk_score += 1
    if steps < 5000:
        risk_score += 1
    if sleep_hours < 6:
        risk_score += 1
    if age > 50:
        risk_score += 1

    # If multiple risk factors → label as anaemia risk
    anaemia = 1 if risk_score >= 3 else 0

    data.append([
        age,
        gender,
        sleep_hours,
        heart_rate,
        spo2,
        steps,
        anaemia
    ])

df = pd.DataFrame(
    data,
    columns=[
        "Age",
        "Gender",
        "SleepHours",
        "HeartRate",
        "SpO2",
        "Steps",
        "Anaemia"
    ]
)

df.to_csv("wearable_anemia_large_dataset.csv", index=False)

print("Large dataset generated successfully with", rows, "rows.")
