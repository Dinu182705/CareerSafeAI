import streamlit as st
import pandas as pd
import pdfplumber
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="CareerSafe AI",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
h1 {
    color: #4CAF50;
}

h2 {
    color: #4CAF50;
}

h3 {
    color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# Load datasets
skills_db = pd.read_csv("dataset/skills.csv")
jobs = pd.read_csv("dataset/jobs.csv")
courses = pd.read_csv("dataset/courses.csv")

skills_db.columns = skills_db.columns.str.strip()
jobs.columns = jobs.columns.str.strip()
courses.columns = courses.columns.str.strip()

# Sidebar
st.sidebar.title("🚀 CareerSafe AI")

st.sidebar.info("""
AI Powered Career Guidance System

✔ Resume Analysis
✔ Skill Detection
✔ Career Matching
✔ Learning Roadmap
✔ Top 3 Career Suggestions
""")

# Main Title
st.title("🚀 CareerSafe AI")
st.markdown("### AI Powered Career Risk Analyzer & Learning Guide")

# Resume Upload
uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

resume_text = ""

if uploaded_file is not None:

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                resume_text += text

if resume_text == "":
    st.warning("Upload a PDF Resume to continue analysis")

# Analyze Button
if st.button("🔍 Analyze Resume"):

    if resume_text == "":

        st.error("Please upload a valid resume PDF")

    else:

        # ------------------------
        # Skill Detection
        # ------------------------

        detected_skills = []

        for skill in skills_db.iloc[:, 0]:

            if skill.lower() in resume_text.lower():

                detected_skills.append(skill)

        # ------------------------
        # Career Analysis
        # ------------------------

        best_job = ""
        best_score = 0
        best_risk = ""

        best_missing = []
        best_courses = []

        career_matches = []

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

            score = (
                matched / len(required)
            ) * 100

            career_matches.append(
                (job, score)
            )

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
                    best_courses = list(set(best_courses))

        career_safe_score = round(
            best_score / 10,
            1
        )

        # ------------------------
        # REPORT OUTPUT
        # ------------------------

        st.success(
            "Analysis Complete 🚀"
        )

        # Dashboard Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🎯 Career Match", f"{best_score:.0f}%")

        with col2:
            st.metric("⚠️ Risk Level", best_risk.split()[0])

        with col3:
            st.metric("🧠 Skills Found", len(detected_skills))

        with col4:
            st.metric("📚 Courses Needed", len(best_courses))

        st.header(
            "📊 Career Report"
        )

        st.subheader(
            "🎯 Detected Skills"
        )

        for skill in detected_skills:

            st.write(
                "✔",
                skill
            )

        st.subheader(
            "💼 Best Career"
        )

        st.success(
            best_job
        )

                # ------------------------
        # TOP 3 CAREERS
        # ------------------------

        career_matches.sort(
            key=lambda x: x[1],
            reverse=True
        )

        st.subheader(
            "🏆 Top 3 Career Matches"
        )

        medals = [
            "🥇",
            "🥈",
            "🥉"
        ]

        for i, (job, score) in enumerate(
            career_matches[:3]
        ):

            st.write(
                f"{medals[i]} {job} - {score:.2f}%"
            )

        # ------------------------
        # SKILLS ANALYTICS
        # ------------------------

        st.subheader("📊 Skills Analytics")

        if detected_skills:

            fig, ax = plt.subplots()

            ax.bar(
                detected_skills,
                [1] * len(detected_skills)
            )

            ax.set_ylabel("Detected")
            ax.set_title("Detected Skills")

            plt.xticks(rotation=45)

            st.pyplot(fig)    

        # ------------------------
        # MATCH SCORE
        # ------------------------
        
        st.subheader(
            "📈 Match Score"
        )

        st.progress(
            int(best_score)
        )

        st.write(
            f"{best_score:.2f}%"
        )

        # ------------------------
        # CAREER RISK
        # ------------------------

        st.subheader(
            "⚠️ Career Risk"
        )

        if "LOW" in best_risk:

            st.success(
                best_risk
            )

        elif "MEDIUM" in best_risk:

            st.warning(
                best_risk
            )

        else:

            st.error(
                best_risk
            )

        # ------------------------
        # SCORE CARD
        # ------------------------

        st.subheader(
            "🏆 CareerSafe Score"
        )

        col1, col2, col3 = st.columns(3)

        with col2:

            st.metric(
                "Score",
                f"{career_safe_score}/10"
            )

        # ------------------------
        # SKILLS TO LEARN
        # ------------------------

        st.subheader(
            "🧠 Skills To Learn"
        )

        if best_missing:

            for skill in best_missing:

                st.write(
                    "✖",
                    skill
                )

        else:

            st.success(
                "No Skill Gaps Found"
            )

        # ------------------------
        # COURSES
        # ------------------------

        st.subheader(
            "📚 Recommended Courses"
        )

        if best_courses:

            for course in best_courses:

                st.write(
                    "📘",
                    course
                )

        else:

            st.success(
                "No courses required"
            )

        # ------------------------
        # ROADMAP
        # ------------------------

        st.subheader(
            "🗺️ Learning Roadmap"
        )

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

        # ------------------------
        # DOWNLOAD REPORT
        # ------------------------

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

# ------------------------
# FOOTER
# ------------------------


st.markdown("---")

st.markdown("""
### 🚀 CareerSafe AI v1.0

Developed using:
- Python
- Streamlit
- Pandas
- PDFPlumber
- Matplotlib

© 2026 CareerSafe AI
""")