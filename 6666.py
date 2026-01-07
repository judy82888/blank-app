import streamlit as st
import datetime
from datetime import timedelta

# ===================== 基础养护指南数据（修复逻辑）=====================
CARE_GUIDES = {
    "dog": {
        "name": "狗狗",
        "feeding": "每日2次（早晚各1次），幼犬可增至3次，避免巧克力、葡萄、洋葱",
        "water": "全天候提供干净饮用水，每日更换",
        "exercise": "小型犬每日1次散步（30分钟），大型犬每日2次（每次1小时）",
        "note": "定期驱虫（每月1次），避免过度喂食导致肥胖",
        "emergency": "拒食处理：先停喂零食，观察24小时，异常及时就医"
    },
    "cat": {
        "name": "猫咪",
        "feeding": "每日2次（早晚），猫粮为主，可搭配少量湿粮，不喂生肉（新手）",
        "water": "每日更换饮用水，建议用流动水碗提高饮水量",
        "grooming": "短毛猫每周梳毛1次，长毛猫每周3次",
        "note": "猫砂盆每日清理，每周彻底清洗",
        "emergency": "拒食处理：停喂零食，观察24小时，出现呕吐/腹泻立即就医"
    },
    "succulent": {
        "name": "多肉植物",
        "watering": "春秋（生长期）：7-10天1次，夏季：15-20天1次（避高温），冬季：20-30天1次（保暖）",
        "light": "每日4-6小时散射光，避免强光直射（夏季遮阳）",
        "soil": "用多肉专用颗粒土（透气防烂根），盆底铺陶粒",
        "note": "浇水遵循「干透浇透」，避免叶心积水",
        "emergency": "烂根处理：停水通风，剪掉腐烂根系，更换新颗粒土，晾干后重新栽种"
    }
}

# 初始化任务（修复session_state）
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ===================== 核心功能（修复变量名+空值处理）=====================
def add_task(task_name, care_type, frequency):
    today = datetime.date.today()  # 修复：定义today
    if frequency == "每日":
        next_due = today + timedelta(days=1)
        freq_code = "daily"
    elif frequency == "每周":
        next_due = today + timedelta(weeks=1)
        freq_code = "weekly"
    elif frequency == "每10天":
        next_due = today + timedelta(days=10)
        freq_code = "10days"
    else:
        return "❌ 频率错误"
    
    st.session_state.tasks.append({
        "name": task_name,
        "type": care_type,
        "frequency": freq_code,
        "frequency_show": frequency,
        "last_done": None,
        "next_due": next_due
    })
    return f"✅ 已添加任务：{task_name}，下次执行：{next_due.strftime('%Y-%m-%d')}"

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
        return f"✅ 已完成任务"
    except IndexError:
        return "❌ 任务序号错误"

def generate_travel_list(travel_days, caregiver_name, emergency_contact):
    today = datetime.date.today()  # 修复：定义today
    end_date = today + timedelta(days=travel_days)
    list_text = f"""
### 📤 旅行代养清单
**时间**：{today.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}
**代养人**：{caregiver_name}
**紧急联系人**：{emergency_contact}

"""
    # 分类任务（修复空值）
    dog_tasks = [t for t in st.session_state.tasks if t["type"] == "dog"]
    cat_tasks = [t for t in st.session_state.tasks if t["type"] == "cat"]
    succulent_tasks = [t for t in st.session_state.tasks if t["type"] == "succulent"]

    # 狗狗部分（修复空值）
    if dog_tasks:
        list_text += f"""
#### 🐶 狗狗养护
**基础要求**：{CARE_GUIDES['dog']['feeding']} | {CARE_GUIDES['dog']['water']}
**任务**：
"""
        for task in dog_tasks:
            list_text += f"- {task['name']}：每{task['frequency_show']}1次\n"
    
    # 猫咪部分
    if cat_tasks:
        list_text += f"""
#### 🐱 猫咪养护
**基础要求**：{CARE_GUIDES['cat']['feeding']} | {CARE_GUIDES['cat']['water']}
**任务**：
"""
        for task in cat_tasks:
            list_text += f"- {task['name']}：每{task['frequency_show']}1次\n"
    
    # 多肉部分
    if succulent_tasks:
        list_text += f"""
#### 🌵 多肉养护
**基础要求**：{CARE_GUIDES['succulent']['watering']} | {CARE_GUIDES['succulent']['light']}
**任务**：
"""
        for task in succulent_tasks:
            list_text += f"- {task['name']}：每{task['frequency_show']}1次\n"
    
    # 紧急提醒（修复空值）
    list_text += f"""
#### ⚠️ 重要提醒
1. 严格按频率执行，避免过度/遗漏养护
2. 异常情况及时联系紧急联系人
3. 应急处理：
"""
    if dog_tasks:
        list_text += f"   - 狗狗：{CARE_GUIDES['dog']['emergency']}\n"
    if cat_tasks:
        list_text += f"   - 猫咪：{CARE_GUIDES['cat']['emergency']}\n"
    if succulent_tasks:
        list_text += f"   - 多肉：{CARE_GUIDES['succulent']['emergency']}\n"

    return list_text

# ===================== 网页界面（修复下载文件名）=====================
st.set_page_config(page_title="养护工具", page_icon="🌿")
st.title("🌿 猫狗+多肉养护工具")

with st.sidebar:
    selected = st.radio("功能菜单", ["查看指南", "添加任务", "待办任务", "代养清单"])

# 1. 查看指南
if selected == "查看指南":
    care_type = st.selectbox("选择品类", ["狗狗（dog）", "猫咪（cat）", "多肉（succulent）"])
    key = care_type.split("（")[1].replace("）", "")
    guide = CARE_GUIDES[key]
    st.write(f"### {guide['name']} 养护规则")
    for k, v in guide.items():
        if k not in ["name", "emergency"]:
            st.write(f"- {k.replace('_', ' ').title()}：{v}")
    st.write(f"### 应急处理：{guide['emergency']}")

# 2. 添加任务
elif selected == "添加任务":
    task_name = st.text_input("任务名称（如：给狗喂食）")
    care_type = st.selectbox("品类", ["dog", "cat", "succulent"])
    freq = st.selectbox("频率", ["每日", "每周", "每10天"]) if care_type == "succulent" else st.selectbox("频率", ["每日", "每周"])
    if st.button("添加任务"):
        if task_name:
            st.success(add_task(task_name, care_type, freq))
        else:
            st.error("任务名称不能为空")

# 3. 待办任务
elif selected == "待办任务":
    today = datetime.date.today()
    st.write(f"### 📅 今日任务（{today.strftime('%Y-%m-%d')}）")
    today_tasks = [t for t in st.session_state.tasks if t["next_due"] == today]
    if today_tasks:
        for i, t in enumerate(today_tasks):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"{i+1}. {t['name']}（{CARE_GUIDES[t['type']]['name']}）")
            with col2:
                if st.button("完成", key=f"done_{i}"):
                    st.success(complete_task(i))
    else:
        st.write("暂无今日任务")

# 4. 代养清单（修复下载文件名）
elif selected == "代养清单":
    travel_days = st.number_input("旅行天数", min_value=1, value=7)
    caregiver = st.text_input("代养人姓名")
    contact = st.text_input("紧急联系人（姓名+电话）")
    if st.button("生成清单"):
        if caregiver and contact and st.session_state.tasks:
            list_text = generate_travel_list(travel_days, caregiver, contact)
            st.markdown(list_text)
            # 修复：定义today后再用
            today = datetime.date.today()
            st.download_button(
                label="下载清单",
                data=list_text,
                file_name=f"代养清单_{today.strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:
            st.error("请填写完整信息并添加任务")
