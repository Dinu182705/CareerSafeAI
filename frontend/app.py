import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CareerSafe AI",
    page_icon="🚀",
    layout="wide"
)

# Load datasets
skills_db = pd.read_csv("../dataset/skills.csv")
jobs = pd.read_csv("../dataset/jobs.csv")
courses = pd.read_csv("../dataset/courses.csv")

# Sidebar
st.sidebar.title("🚀 CareerSafe AI")

st.sidebar.info("""
CareerSafe AI helps students identify:

✔ Best Career Path

✔ Skill Gaps

✔ Career Risk

✔ Learning Roadmap
""")

# Main UI
st.title("🚀 CareerSafe AI")
st.markdown("### AI Powered Career Risk Analyzer & Learning Guide")

resume_text = st.text_area(
    "📄 Paste Your Resume Here",
    height=200
)

if st.button("🔍 Analyze Resume"):

    detected_skills = []

    for skill in skills_db["skill_name"]:
        if skill.lower() in resume_text.lower():
            detected_skills.append(skill)

    best_job = ""
    best_score = 0
    best_risk = ""
    best_missing = []
    best_courses = []

    for _, row in jobs.iterrows():

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

                result = courses[
                    courses["skill_covered"] == skill
                ]

                for _, course in result.iterrows():
                    best_courses.append(
                        course["course_name"]
                    )

    career_safe_score = round(
        best_score / 10,
        1
    )

    st.success("✅ Analysis Complete!")

    st.header("📊 Career Report")

    st.subheader("🎯 Detected Skills")

    for skill in detected_skills:
        st.write("✔", skill)

    st.subheader("💼 Best Career")

    st.success(best_job)

    st.subheader("📈 Match Score")

    st.progress(int(best_score))

    st.write(f"{best_score:.2f}%")

    st.subheader("⚠️ Career Risk")

    if "LOW" in best_risk:
        st.success(best_risk)

    elif "MEDIUM" in best_risk:
        st.warning(best_risk)

    else:
        st.error(best_risk)

    st.subheader("🏆 CareerSafe Score")

    col1, col2, col3 = st.columns(3)

    with col2:
        st.metric(
            label="Score",
            value=f"{career_safe_score}/10"
        )

    st.subheader("🧠 Skills To Learn")

    if best_missing:
        for skill in best_missing:
            st.write("✖", skill)
    else:
        st.success("No Skill Gaps Found")

    st.subheader("📚 Recommended Courses")

    if best_courses:
        for course in best_courses:
            st.write("📘", course)
    else:
        st.success("No courses required")

    st.subheader("🗺️ Learning Roadmap")

    if best_courses:

        week = 1

        for course in best_courses:

            st.write(
                f"Week {week}: {course}"
            )

            week += 1

    else:
        st.success(
            "🚀 You are already career ready!"
        )

    report = f"""
CAREERSAFE AI REPORT

Best Career: {best_job}

Match Score: {best_score:.2f}%

Career Risk: {best_risk}

CareerSafe Score: {career_safe_score}/10
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="CareerSafe_Report.txt",
        mime="text/plain"
    )

st.markdown("---")
st.caption(
    "Built with ❤️ using Python, Streamlit & AI"
)