import streamlit as st
import pandas as pd

# Load datasets
skills_db = pd.read_csv("../dataset/skills.csv")
jobs = pd.read_csv("../dataset/jobs.csv")
courses = pd.read_csv("../dataset/courses.csv")

st.title("🚀 CareerSafe AI")
st.subheader("AI Career Risk Analyzer")

resume_text = st.text_area("Paste Your Resume Here")

if st.button("Analyze Resume"):

    # Detect Skills
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

    career_safe_score = round(best_score / 10, 1)

    # Display Report
    st.success("Analysis Complete!")

    st.header("📊 Career Report")

    st.subheader("Detected Skills")
    for skill in detected_skills:
        st.write("✔", skill)

    st.subheader("Best Career")
    st.write(best_job)

    st.subheader("Match Score")
    st.write(f"{best_score:.2f}%")

    st.subheader("Career Risk")
    st.write(best_risk)

    st.subheader("CareerSafe Score")
    st.write(f"{career_safe_score}/10")

    st.subheader("Skills To Learn")

    if best_missing:
        for skill in best_missing:
            st.write("✖", skill)
    else:
        st.write("None")

    st.subheader("Recommended Courses")

    if best_courses:
        for course in best_courses:
            st.write("-", course)
    else:
        st.write("No courses required")

    st.subheader("Learning Roadmap")

    if best_courses:

        week = 1

        for course in best_courses:
            st.write(f"Week {week}: {course}")
            week += 1

    else:
        st.success("You are already career ready! 🚀")