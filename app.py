import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Placement Prep Tracker",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
/* Main page */
.stApp {
    background-color: #f1f5f9;
    color: #1e293b;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Make all regular text readable */
.stApp,
.stApp p,
.stApp label,
.stApp li,
.stApp span,
.stApp div[data-testid="stMarkdownContainer"] {
    color: #1e293b;
}

/* Headings */
h1, h2, h3, h4, h5 {
    color: #172554 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #e2e8f0;
}

section[data-testid="stSidebar"] * {
    color: #1e293b;
}

/* Header banner */
.hero {
    background: linear-gradient(120deg, #172554, #4338ca);
    padding: 28px;
    border-radius: 18px;
    color: #ffffff;
    margin-bottom: 22px;
}

.hero h1 {
    color: #ffffff !important;
}

.hero p {
    color: #e0e7ff !important;
}

/* Statistics cards */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06);
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] label *,
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: #0f172a !important;
}

/* Task cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff;
    border-radius: 12px;
    border-color: #cbd5e1;
}
/* Text input */
.stTextInput input {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
}

/* Selected dropdown value */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-color: #cbd5e1 !important;
}

/* Selected value and dropdown text */
.stSelectbox div[data-baseweb="select"] span {
    color: #0f172a !important;
}

/* Dropdown arrow */
.stSelectbox div[data-baseweb="select"] svg {
    fill: #334155 !important;
    color: #334155 !important;
}

/* Dropdown options menu */
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background-color: #ffffff !important;
}

div[role="option"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
}

/* Hovered dropdown option */
div[role="option"]:hover {
    background-color: #dbeafe !important;
    color: #0f172a !important;
}

/* Checkbox text */
.stCheckbox label,
.stCheckbox label p {
    color: #1e293b !important;
}

/* Progress bars */
div[data-testid="stProgress"] {
    background-color: #dbeafe;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    border-radius: 8px;
    font-weight: 600;
}

/* Captions and small labels */
.stCaption,
[data-testid="stCaptionContainer"] {
    color: #475569 !important;
}

/* Divider */
hr {
    border-color: #cbd5e1;
}
</style>
""", unsafe_allow_html=True)

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "title": "Solve 2 Python problems", "category": "Coding", "done": False},
        {"id": 2, "title": "Practice aptitude questions", "category": "Aptitude", "done": False},
        {"id": 3, "title": "Prepare self-introduction", "category": "Interview", "done": False},
        {"id": 4, "title": "Revise Python lists", "category": "Coding", "done": True}
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 5

with st.sidebar:
    st.title("🎯 Prep Tracker")
    st.caption("Your placement preparation workspace")
    st.divider()
    st.subheader("➕ Add a task")

    with st.form("add_task_form", clear_on_submit=True):
        new_title = st.text_input("Task name")
        new_category = st.selectbox(
            "Category",
            ["Coding", "Aptitude", "Interview", "Projects", "Resume"]
        )
        submitted = st.form_submit_button("Add task", use_container_width=True)

    if submitted:
        if new_title.strip():
            st.session_state.tasks.append({
                "id": st.session_state.next_id,
                "title": new_title.strip(),
                "category": new_category,
                "done": False
            })
            st.session_state.next_id += 1
            st.rerun()
        else:
            st.warning("Please enter a task name.")

st.markdown("""
<div class="hero">
    <h1>🎯 Placement Preparation Tracker</h1>
    <p>Plan your practice. Track your progress. Get placement-ready.</p>
</div>
""", unsafe_allow_html=True)

st.write(f"📅 Today: {date.today().strftime('%d %B %Y')}")

tasks = st.session_state.tasks
total = len(tasks)
completed = sum(1 for task in tasks if task["done"])
pending = total - completed
progress = completed / total if total else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("📚 Total Tasks", total)
c2.metric("✅ Completed", completed)
c3.metric("⏳ Pending", pending)
c4.metric("📈 Completion", f"{progress * 100:.0f}%")

st.progress(progress, text="Overall preparation progress")

st.subheader("📊 Progress by category")
category_cols = st.columns(5)
categories = ["Coding", "Aptitude", "Interview", "Projects", "Resume"]

for col, category in zip(category_cols, categories):
    items = [t for t in tasks if t["category"] == category]
    done_count = sum(1 for t in items if t["done"])
    with col:
        st.write(f"**{category}**")
        st.caption(f"{done_count}/{len(items)} completed")
        st.progress(done_count / len(items) if items else 0)

st.divider()
st.subheader("📝 Your preparation tasks")

filter_option = st.selectbox(
    "Filter tasks",
    ["All Tasks", "Pending", "Completed"] + categories
)

for task in list(st.session_state.tasks):
    if filter_option == "Pending" and task["done"]:
        continue
    if filter_option == "Completed" and not task["done"]:
        continue
    if filter_option in categories and task["category"] != filter_option:
        continue

    with st.container(border=True):
        col1, col2, col3 = st.columns([5, 2, 1])

        with col1:
            task["done"] = st.checkbox(
                task["title"],
                value=task["done"],
                key=f"task_{task['id']}"
            )

        with col2:
            st.caption(task["category"])
            st.caption("Completed" if task["done"] else "Pending")

        with col3:
            if st.button("🗑️", key=f"delete_{task['id']}"):
                st.session_state.tasks = [
                    t for t in st.session_state.tasks
                    if t["id"] != task["id"]
                ]
                st.rerun()

st.divider()
st.caption("Built with Python and Streamlit 🚀")
