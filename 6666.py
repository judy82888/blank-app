import streamlit as st
import datetime
from datetime import timedelta

# ===================== 基础养护指南数据（猫狗+多肉）=====================
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

# 初始化session state（保存任务，网页刷新不丢失）
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ===================== 核心功能函数 =====================
def add_task(task_name, care_type, frequency):
    """添加养护任务"""
    today = datetime.date.today()
    # 转换频率为天数
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
        return "❌ 频率选择错误！"
    
    task = {
        "name": task_name,
        "type": care_type,
        "frequency": freq_code,
        "frequency_show": frequency,  # 用于展示的频率文字
        "last_done": None,
        "next_due": next_due
    }
    st.session_state.tasks.append(task)
    return f"✅ 已添加任务：{task_name}（{CARE_GUIDES[care_type]['name']}），下次执行时间：{next_due.strftime('%Y-%m-%d')}"

def complete_task(task_index):
    """标记任务完成"""
    try:
        task = st.session_state.tasks[task_index]
        today = datetime.date.today()
        task["last_done"] = today
        # 更新下次执行时间
        if task["frequency"] == "daily":
            task["next_due"] = today + timedelta(days=1)
        elif task["frequency"] == "weekly":
            task["next_due"] = today + timedelta(weeks=1)
        elif task["frequency"] == "10days":
            task["next_due"] = today + timedelta(days=10)
        return f"✅ 已完成任务：{task['name']}，下次执行时间：{task['next_due'].strftime('%Y-%m-%d')}"
    except IndexError:
        return "❌ 任务序号错误！"

def generate_travel_list(travel_days, caregiver_name, emergency_contact):
    """生成旅行代养清单（可视化文本）"""
    today = datetime.date.today()
    end_date = today + timedelta(days=travel_days)
    list_text = f"""
### 📤 旅行代养清单
**时间**：{today.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}
**代养人**：{caregiver_name}
**紧急联系人**：{emergency_contact}

"""
    # 按品类分组
    dog_tasks = [t for t in st.session_state.tasks if t["type"] == "dog"]
    cat_tasks = [t for t in st.session_state.tasks if t["type"] == "cat"]
    succulent_tasks = [t for t in st.session_state.tasks if t["type"] == "succulent"]
    
    if dog_tasks:
        list_text += f"""
#### 🐶 狗狗养护
**基础要求**：{CARE_GUIDES['dog']['feeding']} | {CARE_GUIDES['dog']['water']}
**旅行期间任务**：
"""
        for task in dog_tasks:
            list_text += f"- {task['name']}：每{task['frequency_show']}1次\n"
    
    if cat_tasks:
        list_text += f"""
#### 🐱 猫咪养护
**基础要求**：{CARE_GUIDES['cat']['feeding']} | {CARE_GUIDES['cat']['water']}
**旅行期间任务**：
"""
        for task in cat_tasks:
            list_text += f"- {task['name']}：每{task['frequency_show']}1次\n"
    
    if succulent_tasks:
        list_text += f"""
#### 🌵 多肉养护
**基础要求**：{CARE_GUIDES['succulent']['watering']} | {CARE_GUIDES['succulent']['light']}
**旅行期间任务**：
"""
        for task in succulent_tasks:
            list_text += f"- {task['name']}：每{task['frequency_show']}1次\n"
    
    list_text += f"""
#### ⚠️ 重要提醒
1. 严格按照频率执行，避免过度养护或遗漏
2. 若发现异常（如宠物拒食、多肉腐烂），请及时联系紧急联系人
3. 应急处理：
   - 狗狗/猫咪：{CARE_GUIDES['dog']['emergency'] if dog_tasks else CARE_GUIDES['cat']['emergency']}
   - 多肉：{CARE_GUIDES['succulent']['emergency'] if succulent_tasks else ''}
"""
    return list_text

# ===================== 网页可视化界面 =====================
st.set_page_config(page_title="猫狗+多肉养护工具", page_icon="🌿", layout="wide")
st.title("🌿 猫狗+多肉养护工具")

# 侧边栏：功能菜单
with st.sidebar:
    st.header("功能菜单")
    selected_func = st.radio("请选择功能", ["查看养护指南", "添加养护任务", "查看待办任务", "生成旅行代养清单"])

# 1. 查看养护指南
if selected_func == "查看养护指南":
    st.subheader("📖 基础养护指南")
    care_type = st.selectbox("选择养护品类", ["狗狗（dog）", "猫咪（cat）", "多肉（succulent）"])
    # 转换选择值为代码里的key
    care_type_key = care_type.split("（")[1].replace("）", "")
    guide = CARE_GUIDES[care_type_key]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**🐾 {guide['name']} 核心养护规则**")
        for key, value in guide.items():
            if key not in ["name", "emergency"]:
                st.write(f"- {key.replace('_', ' ').title()}：{value}")
    with col2:
        st.write(f"**🚨 应急处理指南**")
        st.write(guide['emergency'])

# 2. 添加养护任务
elif selected_func == "添加养护任务":
    st.subheader("➕ 添加养护任务")
    task_name = st.text_input("任务名称（如：给金毛喂食、多肉浇水）", placeholder="请输入任务名称")
    care_type = st.selectbox("养护品类", ["狗狗（dog）", "猫咪（cat）", "多肉（succulent）"])
    care_type_key = care_type.split("（")[1].replace("）", "")
    
    # 按品类显示频率选项
    if care_type_key in ["dog", "cat"]:
        frequency = st.selectbox("执行频率", ["每日", "每周"])
    else:
        frequency = st.selectbox("执行频率", ["每10天", "每周"])
    
    if st.button("添加任务"):
        if not task_name:
            st.error("❌ 任务名称不能为空！")
        else:
            result = add_task(task_name, care_type_key, frequency)
            st.success(result)

# 3. 查看待办任务
elif selected_func == "查看待办任务":
    st.subheader("📅 待办任务")
    today = datetime.date.today()
    
    # 筛选今日任务和即将到期任务
    today_tasks = [t for t in st.session_state.tasks if t["next_due"] == today]
    soon_tasks = [t for t in st.session_state.tasks if today < t["next_due"] <= today + timedelta(days=3)]
    
    if today_tasks:
        st.write("### 🚨 今日需执行")
        for i, task in enumerate(today_tasks):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"{i+1}. {task['name']}（{CARE_GUIDES[task['type']]['name']}）")
            with col2:
                if st.button("标记完成", key=f"today_{i}"):
                    result = complete_task(i)
                    st.experimental_rerun()  # 刷新页面
    
    if soon_tasks:
        st.write("### ⚠️ 3天内即将到期")
        for i, task in enumerate(soon_tasks):
            st.write(f"{i+1}. {task['name']} - 到期时间：{task['next_due'].strftime('%Y-%m-%d')}")
    
    if not st.session_state.tasks:
        st.write("暂无任务，快去添加吧！")

# 4. 生成旅行代养清单
elif selected_func == "生成旅行代养清单":
    st.subheader("✈️ 生成旅行代养清单")
    travel_days = st.number_input("旅行天数", min_value=1, max_value=30, value=7)
    caregiver_name = st.text_input("代养人姓名", placeholder="请输入代养人姓名")
    emergency_contact = st.text_input("紧急联系人（姓名+电话）", placeholder="如：张三 138XXXX1234")
    
    if st.button("生成清单"):
        if not caregiver_name or not emergency_contact:
            st.error("❌ 代养人姓名和紧急联系人不能为空！")
        elif not st.session_state.tasks:
            st.error("❌ 暂无养护任务，无法生成清单！")
        else:
            list_text = generate_travel_list(travel_days, caregiver_name, emergency_contact)
            st.markdown(list_text)
            # 添加复制按钮
            st.download_button(
                label="📥 下载清单（文本文件）",
                data=list_text,
                file_name=f"旅行代养清单_{today.strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
