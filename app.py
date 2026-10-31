import streamlit as st
import pandas as pd
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
