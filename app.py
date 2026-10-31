import streamlit as st
import pandas as pd
import time
import json
import os
from io import BytesIO

DATA_FILE = "data.json"

# Load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    return {
        "tasks": [],
        "productive_minutes": 0,
        "waste_minutes": 0,
        "journal": ""
    }

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()
if "subjects" not in data:

    data["subjects"] = {
        "Physics": 0,
        "Chemistry": 0,
        "Maths": 0,
        "Coding": 0
    }
    if "study_history" not in data:
    data["study_history"] = []

    save_data(data)
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "time_left" not in st.session_state:
    st.session_state.time_left = 25 * 60
st.set_page_config(
    page_title="Winter Arc OS",
    layout="wide"
)

st.title("❄️ Winter Arc Life OS")

# Dashboard
st.header("🔥 Dashboard")

completed = len(
    [t for t in data["tasks"] if t["completed"]]
)

total = len(data["tasks"])

score = 0

if (
    data["productive_minutes"]
    + data["waste_minutes"]
) > 0:
    score = int(
        data["productive_minutes"]
        /
        (
            data["productive_minutes"]
            + data["waste_minutes"]
        )
        * 100
    )

c1, c2, c3, c4 = st.columns(4)

c1.metric("Tasks", f"{completed}/{total}")
c2.metric(
    "Productive",
    data["productive_minutes"]
)
c3.metric(
    "Waste",
    data["waste_minutes"]
)
c4.metric("Score %", score)

st.divider()

# Tasks
st.header("✅ Tasks")

task = st.text_input(
    "Enter a new task"
)

if st.button("Add Task") and task:

    data["tasks"].append({
        "name": task,
        "completed": False
    })

    save_data(data)
    st.rerun()

for i, t in enumerate(data["tasks"]):

    done = st.checkbox(
        t["name"],
        value=t["completed"],
        key=f"task_{i}"
    )

    if done != t["completed"]:
        data["tasks"][i]["completed"] = done
        save_data(data)

st.divider()

st.header("🍅 Pomodoro Timer")

minutes = st.session_state.time_left // 60
seconds = st.session_state.time_left % 60

st.markdown(
    f"## ⏳ {minutes:02}:{seconds:02}"
)

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("▶ Start"):
        st.session_state.timer_running = True

with c2:
    if st.button("⏸ Pause"):
        st.session_state.timer_running = False

with c3:
    if st.button("🔄 Reset"):
        st.session_state.timer_running = False
        st.session_state.time_left = 25 * 60

if st.session_state.timer_running:

    time.sleep(1)

    st.session_state.time_left -= 1

    if st.session_state.time_left <= 0:

        st.session_state.time_left = 25 * 60

        data["productive_minutes"] += 25

        save_data(data)

        st.success(
            "🎉 Focus Session Completed!"
        )

    st.rerun()
# Productivity
st.header("⏱ Productivity Tracker")

col1, col2 = st.columns(2)

with col1:
    if st.button("+25 Productive Minutes"):
        data["productive_minutes"] += 25
        save_data(data)
        st.rerun()

with col2:
    if st.button("+10 Waste Minutes"):
        data["waste_minutes"] += 10
        save_data(data)
        st.rerun()

st.divider()

st.header("🏆 Habit Tracker")

habits = [
    "Workout",
    "Reading",
    "Water Goal",
    "Sleep Goal",
    "No Social Media"
]

for habit in habits:
    st.checkbox(habit)
st.divider()

st.header("📚 Study Tracker")

subject = st.selectbox(
    "Subject",
    [
        "Physics",
        "Chemistry",
        "Maths",
        "Coding"
    ]
)

minutes = st.number_input(
    "Minutes Studied",
    min_value=0,
    max_value=600,
    step=5
)

if st.button("Add Study Session"):

    data["subjects"][subject] += minutes

    data["study_history"].append(
        {
            "subject": subject,
            "minutes": minutes
        }
    )

    save_data(data)

    st.success(
        f"{minutes} min added to {subject}"
    )

    st.success(
        f"{minutes} min added to {subject}"
    )

st.subheader("Today's Subjects")

for name, mins in data["subjects"].items():

    st.write(
        f"{name}: {mins} min"
    )
    st.divider()

st.header("📊 Study Analytics")

total_minutes = sum(
    data["subjects"].values()
)

st.metric(
    "Total Study Time",
    f"{total_minutes} min"
)

for subject, mins in data["subjects"].items():

    st.write(
        f"### {subject}"
    )

    progress = min(
        mins / 600,
        1.0
    )

    st.progress(progress)

    st.write(
        f"{mins} minutes"
    )
    import pandas as pd

st.subheader(
    "📈 Study Chart"
)

chart_data = pd.DataFrame(
    {
        "Minutes":
        data["subjects"]
    }
)

st.bar_chart(chart_data)
best_subject = max(
    data["subjects"],
    key=data["subjects"].get
)

st.success(
    f"🏆 Best Subject: {best_subject}"
)
st.divider()

st.header("📅 Weekly Study Report")

weekly_total = 0

for session in data["study_history"]:
    weekly_total += session["minutes"]

st.metric(
    "Weekly Minutes",
    weekly_total
)

st.subheader("🏆 Subject Rankings")

ranked = sorted(
    data["subjects"].items(),
    key=lambda x: x[1],
    reverse=True
)

for i, item in enumerate(ranked):

    subject = item[0]
    mins = item[1]

    st.write(
        f"{i+1}. {subject} — {mins} min"
    )
    st.subheader("🤖 Productivity Insights")

if weekly_total >= 1000:
    st.success(
        "🔥 Excellent consistency this week!"
    )

elif weekly_total >= 500:
    st.info(
        "✅ Good progress. Keep pushing."
    )

else:
    st.warning(
        "⚠️ Try increasing study hours next week."
    )

strongest = ranked[0][0]

st.write(
    f"Strongest Subject: {strongest}"
)
# Journal
st.header("📔 Daily Journal")

journal = st.text_area(
    "Write your thoughts",
    value=data["journal"]
)

if st.button("Save Journal"):
    data["journal"] = journal
    save_data(data)
    st.success("Journal Saved!")

st.divider()

# Excel Export
st.header("📊 Export Excel")

if st.button("Generate Report"):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        pd.DataFrame(
            data["tasks"]
        ).to_excel(
            writer,
            sheet_name="Tasks",
            index=False
        )

    st.download_button(
        label="⬇ Download Excel",
        data=output.getvalue(),
        file_name="WinterArc.xlsx",
        mime="application/vnd.ms-excel"
    )

st.divider()

st.header("🎯 Daily Score")

task_score = 0

for task in data["tasks"]:
    if task["completed"]:
        task_score += 10

habit_score = 0

for habit in habits:
    habit_score += 10

focus_score = data["productive_minutes"] // 25 * 5

daily_score = min(
    task_score +
    habit_score +
    focus_score,
    100
)

st.metric(
    "Today's Score",
    f"{daily_score}/100"
)
# AI Coach
st.header("🤖 AI Coach")

if score >= 80:
    st.success(
        "🔥 Beast Mode! Keep going!"
    )
elif score >= 60:
    st.info(
        "✅ Good progress. Reduce distractions."
    )
else:
    st.warning(
        "⚠️ Focus more tomorrow."
    )
