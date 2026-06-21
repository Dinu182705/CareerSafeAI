import pandas as pd

skills_db = pd.read_csv("../dataset/skills.csv")

resume_text = input("Paste your resume text:\n")

detected_skills = []

for skill in skills_db["skill_name"]:

    if skill.lower() in resume_text.lower():
        detected_skills.append(skill)

print("Detected Skills:")
print(detected_skills)