import pandas as pd

jobs = pd.read_csv("../dataset/jobs.csv")

user_skills = ["Python", "SQL"]

print("Your Skills:", user_skills)
print()

for index, row in jobs.iterrows():

    job = row["job_role"]
    required = row["required_skills"].split(",")

    matched = 0
    missing = []

    for skill in required:

        skill = skill.strip()

        if skill in user_skills:
            matched += 1
        else:
            missing.append(skill)

    score = (matched / len(required)) * 100

    if score >= 80:
        risk = "LOW 🟢"
    elif score >= 50:
        risk = "MEDIUM 🟡"
    else:
        risk = "HIGH 🔴"

    print(f"\n{job} : {score:.2f}% Match")
    print("Career Risk:", risk)
    
    if missing:
        print("Missing Skills:", ", ".join(missing))