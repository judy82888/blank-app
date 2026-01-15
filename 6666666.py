import streamlit as st
import datetime
from datetime import timedelta

# ===================== 基础养护指南数据 =====================
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

# 初始化任务（session state）
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ===================== 核心修复：自动刷新任务日期 =====================
def refresh_tasks_by_date():
    """每次打开页面，自动检查系统日期，更新到期任务为今日待办"""
    today = datetime.date.today()
    for task in st.session_state.tasks:
        # 如果任务的下次执行日期 ≤ 今天，自动设为今日待办
        if task["next_due"] <= today:
            task["next_due"] = today

# 页面加载时，先执行日期刷新（关键！）
refresh_tasks_by_date()

# ===================== 核心功能函数 =====================
def add_task(task_name, care_type, frequency):
    today = datetime.date.today()
    if frequency == "Daily":
        next_due = today  # 新增任务当天就显示
        freq_code = "daily"
    elif frequency == "Weekly":
        next_due = today
        freq_code = "weekly"
    elif frequency == "Every 10 Days":
        next_due = today
        freq_code = "10days"
    else:
        return "❌ Invalid frequency"
    
    new_task = {
        "name": task_name,
        "type": care_type,
        "frequency": freq_code,
        "frequency_show": frequency,
        "last_done": None,
        "next_due": next_due
    }
    st.session_state.tasks.append(new_task)
    return f"✅ Task added: {task_name} (Due TODAY: {next_due.strftime('%Y-%m-%d')})"

def complete_task(task_index):
    try:
        task = st.session_state.tasks[task_index]
        today = datetime.date.today()
        task["last_done"] = today
        # 完成后，设置下次执行日期（每日=明天，每周=下周，10天=10天后）
        if task["frequency"] == "daily":
            task["next_due"] = today + timedelta(days=1)
        elif task["frequency"] == "weekly":
            task["next_due"] = today + timedelta(weeks=1)
        elif task["frequency"] == "10days":
            task["next_due"] = today + timedelta(days=10)
        return f"✅ Task completed! Next due: {task['next_due'].strftime('%Y-%m-%d')}"
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
        for succulent_task in succulent_tasks:
            list_text += f"- {succulent_task['name']}: Every {succulent_task['frequency_show']}\n"
    
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

# ===================== 网页界面 =====================
st.set_page_config(page_title="Pet & Plant Care Tool", page_icon="🌿")
st.title("🌿 Pet & Plant Care Tool (Dog/Cat/Succulent)")

with st.sidebar:
    selected = st.radio("Menu", ["View Care Guide", "Add Task", "To-Do Tasks", "Travel Checklist"])

# 1. 查看养护指南
if selected == "View Care Guide":
    care_type = st.selectbox("Select Type", ["dog", "cat", "succulent"])
    guide = CARE_GUIDES[care_type]
    st.write(f"### {guide['name']} Care Rules")
    for k, v in guide.items():
        if k not in ["name", "emergency"]:
            st.write(f"- {k.replace('_', ' ').title()}: {v}")
    st.write(f"### Emergency: {guide['emergency']}")

# 2. 添加任务
elif selected == "Add Task":
    task_name = st.text_input("Task Name (e.g.: Feed dog, Water succulent)")
    care_type = st.selectbox("Type", ["dog", "cat", "succulent"])
    if care_type == "succulent":
        freq = st.selectbox("Frequency", ["Daily", "Weekly", "Every 10 Days"])
    else:
        freq = st.selectbox("Frequency", ["Daily", "Weekly"])
    
    if st.button("Add Task"):
        if task_name:
            result = add_task(task_name, care_type, freq)
            st.success(result)
        else:
            st.error("Task name cannot be empty")

# 3. 今日待办（自动显示到期任务）
elif selected == "To-Do Tasks":
    today = datetime.date.today()
    st.write(f"### 📅 Today's Tasks ({today.strftime('%Y-%m-%d')})")
    # 筛选所有到期的任务（包括前一天加的）
    today_tasks = [t for t in st.session_state.tasks if t["next_due"] == today]
    
    if today_tasks:
        for i, task in enumerate(today_tasks):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"{i+1}. {task['name']} ({CARE_GUIDES[task['type']]['name']})")
            with col2:
                # 获取任务在全局列表的真实索引
                global_index = st.session_state.tasks.index(task)
                if st.button("Complete", key=f"done_{global_index}"):
                    st.success(complete_task(global_index))
                    st.rerun()  # 刷新页面，立即更新待办
    else:
        st.write("No tasks for today! Add a task above.")

# 4. 旅行代养清单
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
