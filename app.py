
import streamlit as st
import pandas as pd

st.set_page_config(page_title="12-Week Fitness Coach", page_icon="💪", layout="centered")

# --- Branding header ---
col1, col2 = st.columns([1,4])
with col1:
    st.image("logo.png", width=72)
with col2:
    st.title("12-Week Fitness Coach")
    st.caption("Dark-mode. Mobile-first. 3 sessions/week • 50' per session")

# Accent style
st.markdown("""
<style>
/* Accent color */
:root, [data-testid="stAppViewContainer"] * {
  --accent: #00B487;
}
a, .st-emotion-cache-1wbqy5l, .st-emotion-cache-1dp5vir, .st-emotion-cache-16idsys { color: var(--accent) !important; }
.st-emotion-cache-1vt4y43, .st-emotion-cache-15hul6a, .stButton>button { border-color: var(--accent) !important; }
.stButton>button { background: rgba(0,180,135,0.12); color: #E6FFF7; border-radius: 8px; }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    workout = pd.read_csv("workout_plan.csv")
    meal = pd.read_csv("meal_plan.csv")
    progress = pd.read_csv("progress_tracker.csv")
    return workout, meal, progress

workout_df, meal_df, progress_df = load_data()

with st.sidebar:
    st.header("Targets")
    st.markdown("""
- Weight: 79 → **67 kg**
- Body Fat: 27% → **~18–20%**
- Frequency: **3x/week**, 50’ per session
- Equipment: Dumbbell • Lat Pulldown • Smith
""")
    st.markdown("---")
    st.write("Data export")
    st.download_button("Workout CSV", workout_df.to_csv(index=False), file_name="workout_plan.csv")
    st.download_button("Meal CSV", meal_df.to_csv(index=False), file_name="meal_plan.csv")
    st.download_button("Progress CSV", progress_df.to_csv(index=False), file_name="progress_tracker.csv")

tab1, tab2, tab3 = st.tabs(["📅 Workout", "🍽️ Meal Plan", "📈 Progress"])

with tab1:
    st.subheader("Weekly Schedule")
    week_list = sorted(workout_df["Week"].unique(), key=lambda x: int(x.split()[-1]))
    selected_week = st.selectbox("Choose Week", week_list, index=0)
    wdf = workout_df[workout_df["Week"] == selected_week]

    for _, row in wdf.iterrows():
        with st.expander(f"{row['Day']} — {row['Focus']}"):
            st.markdown("**Routine:**")
            for it in [x.strip() for x in row["Workout"].split(",")]:
                st.markdown(f"- {it}")
            st.markdown("**Protocol:** 3 sets each, 8–15 reps. Rest 30–60s.")
            st.checkbox(f"Completed: {row['Day']}", key=f"done_{selected_week}_{row['Day']}")

with tab2:
    st.subheader("7-Day Fat Loss Menu (1500–1600 kcal/day)")
    day_names = list(meal_df["Day"].unique())
    sel_day = st.selectbox("Day", day_names, index=0)
    mdf = meal_df[meal_df["Day"] == sel_day]
    st.dataframe(mdf, use_container_width=True)
    st.markdown(f"**Daily total:** {int(mdf['Calories'].sum())} kcal • Protein {int(mdf['Protein (g)'].sum())} g")

with tab3:
    st.subheader("Weekly Check-in")
    p = progress_df.copy()
    week_select = st.selectbox("Week", p["Week"].tolist(), index=0)
    row_idx = p[p["Week"] == week_select].index[0]

    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("Body Weight (kg)", min_value=0.0, value=79.0, step=0.1)
        bodyfat = st.number_input("Body Fat (%)", min_value=0.0, value=27.0, step=0.1)
        energy = st.slider("Energy (1–5)", 1, 5, 3)
    with c2:
        waist = st.number_input("Waist (cm)", min_value=0.0, value=85.0, step=0.5)
        hip = st.number_input("Hip (cm)", min_value=0.0, value=95.0, step=0.5)
        sessions = st.number_input("Workout Sessions", min_value=0, max_value=3, value=0, step=1)

    notes = st.text_area("Notes", value="", height=80)

    if st.button("Save Week Data"):
        p.loc[row_idx, "Body Weight (kg)"] = weight
        p.loc[row_idx, "Body Fat (%)"] = bodyfat
        p.loc[row_idx, "Waist (cm)"] = waist
        p.loc[row_idx, "Hip (cm)"] = hip
        p.loc[row_idx, "Workout Sessions"] = sessions
        p.loc[row_idx, "Energy Level (1-5)"] = energy
        p.loc[row_idx, "Notes"] = notes
        st.session_state["progress_df"] = p
        st.success("Saved in session. Use the download button to export.")

    export_df = st.session_state.get("progress_df", p)
    st.download_button("Download Updated Progress CSV", export_df.to_csv(index=False), file_name="progress_tracker_updated.csv")
