import streamlit as st
import datetime
from datetime import timedelta

# ===================== Basic Care Guide Data =====================
CARE_GUIDES = {
    "dog": {
        "name": "Dog",
        "feeding": "Twice a day (morning/evening), 3 times for puppies. Avoid chocolate/grapes/onions.",
        "water": "Clean water 24/7, replace daily.",
        "exercise": "Small dogs: 30min walk/day; Large dogs: 2×1hr walks/day.",
        "note": "Deworm monthly, avoid overfeeding.",
        "emergency": "Loss of appetite: Stop treats, observe 24hrs, see vet if abnormal."
    },
    "cat": {
        "name": "Cat",
        "feeding": "Twice a day (morning/evening), mainly cat food + small wet food.",
        "water": "Replace water daily, use flowing bowl for more intake.",
        "grooming": "Short-haired: brush 1×/week; Long-haired: brush 3×/week.",
        "note": "Clean litter box daily, wash weekly.",
        "emergency": "Loss of appetite: Stop treats, see vet if vomiting/diarrhea."
    },
    "succulent": {
        "name": "Succulent",
        "watering": "Spring/Fall: 7-10 days; Summer:15-20 days; Winter:20-30 days.",
        "light": "4-6hrs scattered light/day, avoid direct sun in summer.",
        "soil": "Use granular soil, lay ceramsite at pot bottom.",
        "note": "Water only when soil is dry, no water in leaf center.",
        "emergency": "Root rot: Stop watering, cut rotten roots, replant with new soil."
    }
}

# Initialize tasks (same as Chinese version)
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ===================== Core Functions (1:1 copy from working Chinese version) =====================
def add_task(task_name, care_type, frequency):
    today = datetime.date.today()
    if frequency == "Daily":
        next_due = today + timedelta(days=1)
        freq_code = "daily"
    elif frequency == "Weekly":
        next_due = today + timedelta(weeks=1)
        freq_code = "weekly"
    elif frequency == "Every 10 Days":
        next_due = today + timedelta(days=10)
        freq_code = "10days"
    else:
        return "❌ Invalid frequency"
    
    st.session_state.tasks.append({
        "name": task_name,
        "type": care_type,
        "frequency": freq_code,
        "frequency_show": frequency,
        "last_done": None,
        "next_due": next_due
    })
    return f"✅ Task added: {task_name}, Next: {next_due.strftime('%Y-%m-%d')}"

def complete_task(task_index):
    try:
        task = st.session_state.tasks[task_index]
        today = datetime.date.today()
        task["last_done"] = today
        if task["frequency"] == "daily":
            task["next_due"] = today + timedelta(days=1)
        elif task["frequency"] == "weekly":
            task["next_due"] = today + timedelta(weeks=1)
        elif task["frequency"] == "10days":
            task["next_due"] = today + timedelta(days=10)
        return f"✅ Task completed"
    except IndexError:
        return "❌ Invalid task number"

def generate_travel_list(travel_days, caregiver_name, emergency_contact):
    today = datetime.date.today()
    end_date = today + timedelta(days=travel_days)
    list_text = f"""
### 📤 Travel Care Checklist
**Period**: {today.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}
**Caregiver**: {caregiver_name}
**Emergency Contact**: {emergency_contact}

"""
    dog_tasks = [t for t in st.session_state.tasks if t["type"] == "dog"]
    cat_tasks = [t for t in st.session_state.tasks if t["type"] == "cat"]
    succulent_tasks = [t for t in st.session_state.tasks if t["type"] == "succulent"]

    if dog_tasks:
        list_text += f"""
#### 🐶 Dog Care
**Basic Rules**: {CARE_GUIDES['dog']['feeding']} | {CARE_GUIDES['dog']['water']}
**Tasks**:
"""
        for task in dog_tasks:
            list_text += f"- {task['name']}: Every {task['frequency_show']}\n"
    
    if cat_tasks:
        list_text += f"""
#### 🐱 Cat Care
**Basic Rules**: {CARE_GUIDES['cat']['feeding']} | {CARE_GUIDES['cat']['water']}
**Tasks**:
"""
        for task in cat_tasks:
            list_text += f"- {task['name']}: Every {task['frequency_show']}\n"
    
    if succulent_tasks:
        list_text += f"""
#### 🌵 Succulent Care
**Basic Rules**: {CARE_GUIDES['succulent']['watering']} | {CARE_GUIDES['succulent']['light']}
**Tasks**:
"""
        for task in succulent_tasks:
            list_text += f"- {task['name']}: Every {task['frequency_show']}\n"
    
    list_text += f"""
#### ⚠️ Important Reminders
1. Follow frequency strictly (no over/under care)
2. Contact emergency contact if abnormal
3. Emergency Handling:
"""
    if dog_tasks:
        list_text += f"   - Dog: {CARE_GUIDES['dog']['emergency']}\n"
    if cat_tasks:
        list_text += f"   - Cat: {CARE_GUIDES['cat']['emergency']}\n"
    if succulent_tasks:
        list_text += f"   - Succulent: {CARE_GUIDES['succulent']['emergency']}\n"

    return list_text

# ===================== UI (Same logic as working Chinese version) =====================
st.set_page_config(page_title="Care Tool", page_icon="🌿")
st.title("🌿 Pet & Plant Care Tool (Dog/Cat/Succulent)")

with st.sidebar:
    selected = st.radio("Menu", ["View Guide", "Add Task", "To-Do Tasks", "Travel Checklist"])

# 1. View Guide (Fixed mapping issue)
if selected == "View Guide":
    care_type = st.selectbox("Select Type", ["dog", "cat", "succulent"])  # Same as Chinese version
    guide = CARE_GUIDES[care_type]
    st.write(f"### {guide['name']} Care Rules")
    for k, v in guide.items():
        if k not in ["name", "emergency"]:
            st.write(f"- {k.replace('_', ' ').title()}: {v}")
    st.write(f"### Emergency: {guide['emergency']}")

# 2. Add Task (Same as Chinese version)
elif selected == "Add Task":
    task_name = st.text_input("Task Name (e.g.: Feed dog, Water succulent)")
    care_type = st.selectbox("Type", ["dog", "cat", "succulent"])
    if care_type == "succulent":
        freq = st.selectbox("Frequency", ["Daily", "Weekly", "Every 10 Days"])
    else:
        freq = st.selectbox("Frequency", ["Daily", "Weekly"])
    
    if st.button("Add Task"):
        if task_name:
            st.success(add_task(task_name, care_type, freq))
        else:
            st.error("Task name cannot be empty")

# 3. To-Do Tasks (Same as Chinese version)
elif selected == "To-Do Tasks":
    today = datetime.date.today()
    st.write(f"### 📅 Today's Tasks ({today.strftime('%Y-%m-%d')})")
    today_tasks = [t for t in st.session_state.tasks if t["next_due"] == today]
    
    if today_tasks:
        for i, t in enumerate(today_tasks):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"{i+1}. {t['name']} ({CARE_GUIDES[t['type']]['name']})")
            with col2:
                if st.button("Complete", key=f"done_{i}"):
                    st.success(complete_task(i))
    else:
        st.write("No tasks for today")

# 4. Travel Checklist (Same as Chinese version)
elif selected == "Travel Checklist":
    travel_days = st.number_input("Travel Days", min_value=1, value=7)
    caregiver = st.text_input("Caregiver Name")
    contact = st.text_input("Emergency Contact (Name + Phone)")
    
    if st.button("Generate Checklist"):
        if caregiver and contact and st.session_state.tasks:
            list_text = generate_travel_list(travel_days, caregiver, contact)
            st.markdown(list_text)
            today = datetime.date.today()
            st.download_button(
                label="Download Checklist",
                data=list_text,
                file_name=f"Care_Checklist_{today.strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:
            st.error("Fill all info and add tasks first")
