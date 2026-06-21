import pandas as pd

# Load datasets
skills_db = pd.read_csv("../dataset/skills.csv")
jobs = pd.read_csv("../dataset/jobs.csv")
courses = pd.read_csv("../dataset/courses.csv")

# Get resume text from user
resume_text = input("Paste your resume text:\n")

# Detect skills from resume
detected_skills = []

for skill in skills_db["skill_name"]:
    if skill.lower() in resume_text.lower():
        detected_skills.append(skill)

# Career Analysis
best_job = ""
best_score = 0
best_risk = ""
best_missing = []
best_courses = []

for index, row in jobs.iterrows():

    job = row["job_role"]
    required = row["required_skills"].split(",")

    matched = 0
    missing = []

    for skill in required:

        skill = skill.strip()

        if skill in detected_skills:
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

# CareerSafe Score
career_safe_score = round(best_score / 10, 1)

# Final Report
print("\n")
print("=" * 45)
print("           CAREERSAFE AI REPORT")
print("=" * 45)

print("\nDetected Skills:")
for skill in detected_skills:
    print("✔", skill)

print("\nBest Career:")
print(best_job)

print("\nMatch Score:")
print(f"{best_score:.2f}%")

print("\nCareer Risk:")
print(best_risk)

print("\nCareerSafe Score:")
print(f"{career_safe_score}/10")

print("\nStrengths:")
for skill in detected_skills:
    print("✔", skill)

print("\nSkills To Learn:")
if best_missing:
    for skill in best_missing:
        print("✖", skill)
else:
    print("None")

print("\nRecommended Courses:")
if best_courses:
    for course in best_courses:
        print("-", course)
else:
    print("No courses required")

print("\nLearning Roadmap:")

if best_courses:

    week = 1

    for course in best_courses:
        print(f"\nWeek {week}:")
        print("-", course)

        week += 1

else:
    print("You are already career ready! 🚀")

print("\n" + "=" * 45)