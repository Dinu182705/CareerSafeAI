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

print("\nDetected Skills:")
print(detected_skills)

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

# Final Report
print("\n")
print("=" * 40)
print("        CAREERSAFE AI REPORT")
print("=" * 40)

print("\nDetected Skills:")
for skill in detected_skills:
    print("-", skill)

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
else:
    print("None")

print("\nRecommended Courses:")
if best_courses:
    for course in best_courses:
        print("-", course)
else:
    print("No courses required")

print("\n" + "=" * 40)