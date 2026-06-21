import pandas as pd

best_job = ""
best_score = 0
best_risk = ""
best_missing = []
best_courses = []
jobs = pd.read_csv("../dataset/jobs.csv")
courses = pd.read_csv("../dataset/courses.csv")

skills_input = input("Enter your skills (comma separated): ")

user_skills = [skill.strip() for skill in skills_input.split(",")]

print("\nYour Skills:", user_skills)

best_job = ""
best_score = 0
best_risk = ""

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

        print("Recommended Courses:")

        for skill in missing:
            result = courses[courses["skill_covered"] == skill]

            for _, course in result.iterrows():
                print("-", course["course_name"])

    if score > best_score:
       best_score = score
       best_job = job
       best_risk = risk
       best_missing = missing.copy()

       best_courses = []

       for skill in missing:
           result = courses[courses["skill_covered"] == skill]

       for _, course in result.iterrows():
           best_courses.append(course["course_name"])

print("\n")
print("=" * 35)
print("      CAREERSAFE AI REPORT")
print("=" * 35)

print("\nBest Career:")
print(best_job)

print("\nMatch Score:")
print(f"{best_score:.2f}%")

print("\nCareer Risk:")
print(best_risk)

print("\nSkills To Learn:")

if best_missing:
    for skill in best_missing:
        print("-", skill)

print("\nRecommended Courses:")



if best_courses:
    for course in best_courses:
        print("-", course)

print("\n" + "=" * 35)