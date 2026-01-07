import datetime
from datetime import timedelta

# ===================== 基础养护指南数据（猫狗+多肉）=====================
CARE_GUIDES = {
    "dog": {
        "name": "狗狗",
        "feeding": "每日2次（早晚各1次），幼犬可增至3次，避免巧克力、葡萄、洋葱",
        "water": "全天候提供干净饮用水，每日更换",
        "exercise": "小型犬每日1次散步（30分钟），大型犬每日2次（每次1小时）",
        "note": "定期驱虫（每月1次），避免过度喂食导致肥胖"
    },
    "cat": {
        "name": "猫咪",
        "feeding": "每日2次（早晚），猫粮为主，可搭配少量湿粮，不喂生肉（新手）",
        "water": "每日更换饮用水，建议用流动水碗提高饮水量",
        "grooming": "短毛猫每周梳毛1次，长毛猫每周3次",
        "note": "猫砂盆每日清理，每周彻底清洗"
    },
    "succulent": {
        "name": "多肉植物",
        "watering": "春秋（生长期）：7-10天1次，夏季：15-20天1次（避高温），冬季：20-30天1次（保暖）",
        "light": "每日4-6小时散射光，避免强光直射（夏季遮阳）",
        "soil": "用多肉专用颗粒土（透气防烂根），盆底铺陶粒",
        "note": "浇水遵循「干透浇透」，避免叶心积水"
    }
}

# ===================== 工具核心类 =====================
class PetPlantCareTool:
    def __init__(self):
        self.tasks = []  # 存储养护任务：[{name, type, frequency, last_done, next_due}]
    
    # 1. 查询基础养护指南
    def show_care_guide(self, care_type):
        if care_type not in CARE_GUIDES:
            print("❌ 暂无该品类养护指南，支持：dog（狗狗）、cat（猫咪）、succulent（多肉）")
            return
        guide = CARE_GUIDES[care_type]
        print(f"\n🌿 {guide['name']} 基础养护指南")
        for key, value in guide.items():
            if key != "name":
                print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # 2. 添加养护任务（喂食/浇水）
    def add_task(self, task_name, care_type, frequency):
        """
        frequency: 支持 'daily'（每日）、'weekly'（每周）、'10days'（每10天，多肉专用）
        """
        # 计算下次执行时间
        today = datetime.date.today()
        if frequency == "daily":
            next_due = today + timedelta(days=1)
        elif frequency == "weekly":
            next_due = today + timedelta(weeks=1)
        elif frequency == "10days":
            next_due = today + timedelta(days=10)
        else:
            print("❌ 频率支持：daily（每日）、weekly（每周）、10days（每10天）")
            return
        
        task = {
            "name": task_name,
            "type": care_type,
            "frequency": frequency,
            "last_done": None,
            "next_due": next_due
        }
        self.tasks.append(task)
        print(f"\n✅ 已添加任务：{task_name}（{CARE_GUIDES[care_type]['name']}），下次执行时间：{next_due.strftime('%Y-%m-%d')}")
    
    # 3. 查看今日待办+即将到期任务
    def show_tasks(self):
        today = datetime.date.today()
        print(f"\n📅 今日养护任务（{today.strftime('%Y-%m-%d')}）")
        due_soon = []
        for i, task in enumerate(self.tasks, 1):
            if task["next_due"] == today:
                print(f"  {i}. 🚨 待执行：{task['name']}（{task['type']}）")
            elif today < task["next_due"] <= today + timedelta(days=3):
                due_soon.append((i, task))
        
        if due_soon:
            print("\n⚠️  3天内即将到期任务")
            for i, task in due_soon:
                print(f"  {i}. {task['name']}，到期时间：{task['next_due'].strftime('%Y-%m-%d')}")
        
        if not self.tasks:
            print("  暂无任务，快去添加吧！")
    
    # 4. 标记任务完成（更新下次执行时间）
    def complete_task(self, task_index):
        try:
            task = self.tasks[task_index - 1]
            today = datetime.date.today()
            task["last_done"] = today
            # 根据频率更新下次执行时间
            if task["frequency"] == "daily":
                task["next_due"] = today + timedelta(days=1)
            elif task["frequency"] == "weekly":
                task["next_due"] = today + timedelta(weeks=1)
            elif task["frequency"] == "10days":
                task["next_due"] = today + timedelta(days=10)
            print(f"\n✅ 已完成任务：{task['name']}，下次执行时间：{task['next_due'].strftime('%Y-%m-%d')}")
        except IndexError:
            print(f"❌ 任务序号错误，当前共{len(self.tasks)}个任务")
    
    # 5. 生成旅行代养清单（导出为文本，可复制分享）
    def generate_travel_list(self, travel_days, caregiver_name):
        """
        travel_days: 旅行天数
        caregiver_name: 代养人姓名
        """
        today = datetime.date.today()
        end_date = today + timedelta(days=travel_days)
        print(f"\n📤 旅行代养清单（{today.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}）")
        print(f"代养人：{caregiver_name}")
        print("="*50)
        
        # 按品类分组任务
        dog_tasks = [t for t in self.tasks if t["type"] == "dog"]
        cat_tasks = [t for t in self.tasks if t["type"] == "cat"]
        succulent_tasks = [t for t in self.tasks if t["type"] == "succulent"]
        
        if dog_tasks:
            print(f"\n🐶 狗狗养护")
            print(f"  基础要求：{CARE_GUIDES['dog']['feeding']} | {CARE_GUIDES['dog']['water']}")
            print(f"  旅行期间任务：")
            for task in dog_tasks:
                print(f"    - {task['name']}：每{task['frequency'].replace('daily', '天').replace('weekly', '周')}1次")
        
        if cat_tasks:
            print(f"\n🐱 猫咪养护")
            print(f"  基础要求：{CARE_GUIDES['cat']['feeding']} | {CARE_GUIDES['cat']['water']}")
            print(f"  旅行期间任务：")
            for task in cat_tasks:
                print(f"    - {task['name']}：每{task['frequency'].replace('daily', '天').replace('weekly', '周')}1次")
        
        if succulent_tasks:
            print(f"\n🌵 多肉养护")
            print(f"  基础要求：{CARE_GUIDES['succulent']['watering']} | {CARE_GUIDES['succulent']['light']}")
            print(f"  旅行期间任务：")
            for task in succulent_tasks:
                print(f"    - {task['name']}：每{task['frequency'].replace('10days', '10天')}1次")
        
        print(f"\n⚠️  重要提醒：")
        print(f"  1. 严格按照频率执行，避免过度养护或遗漏")
        print(f"  2. 若发现异常（如宠物拒食、多肉腐烂），请及时联系主人")
        print("="*50)

# ===================== 交互入口（用户可直接运行使用）=====================
if __name__ == "__main__":
    tool = PetPlantCareTool()
    print("🎉 猫狗+多肉养护工具启动！")
    
    while True:
        print("\n" + "="*30)
        print("功能菜单：")
        print("1. 查看养护指南（猫狗/多肉）")
        print("2. 添加养护任务（喂食/浇水）")
        print("3. 查看待办任务")
        print("4. 标记任务完成")
        print("5. 生成旅行代养清单")
        print("0. 退出工具")
        print("="*30)
        
        choice = input("请输入功能编号：")
        
        if choice == "1":
            care_type = input("请输入查询类型（dog=狗狗，cat=猫咪，succulent=多肉）：").lower()
            tool.show_care_guide(care_type)
        
        elif choice == "2":
            task_name = input("请输入任务名称（如：给狗狗喂食、多肉浇水）：")
            care_type = input("请输入养护品类（dog=狗狗，cat=猫咪，succulent=多肉）：").lower()
            if care_type not in CARE_GUIDES:
                print("❌ 品类错误，支持 dog/cat/succulent")
                continue
            # 按品类推荐频率
            if care_type in ["dog", "cat"]:
                frequency = input("请输入频率（daily=每日，weekly=每周）：").lower()
            else:
                frequency = input("请输入频率（10days=每10天，weekly=每周）：").lower()
            tool.add_task(task_name, care_type, frequency)
        
        elif choice == "3":
            tool.show_tasks()
        
        elif choice == "4":
            tool.show_tasks()
            if tool.tasks:
                task_index = input("\n请输入要标记完成的任务序号：")
                if task_index.isdigit():
                    tool.complete_task(int(task_index))
                else:
                    print("❌ 请输入数字序号")
        
        elif choice == "5":
            travel_days = input("请输入旅行天数：")
            if not travel_days.isdigit():
                print("❌ 请输入数字")
                continue
            caregiver_name = input("请输入代养人姓名：")
            tool.generate_travel_list(int(travel_days), caregiver_name)
        
        elif choice == "0":
            print("\n👋 再见！祝你的宠物和多肉健康成长～")
            break
        
        else:
            print("❌ 请输入正确的功能编号")