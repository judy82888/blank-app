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

# Initialize tasks
tasks = []

# ===================== Core Functions =====================
def show_care_guide(care_type):
    if care_type not in CARE_GUIDES:
        print("❌ Invalid type! Support: dog / cat / succulent")
        return
    guide = CARE_GUIDES[care_type]
    print(f"\n🌿 {guide['name']} Care Guide")
    for key, value in guide.items():
        if key != "name":
            print(f"  - {key.replace('_', ' ').title()}: {value}")

def add_task(task_name, care_type, frequency):
    today = datetime.date.today()
    if frequency == "daily":
        next_due = today + timedelta(days=1)
    elif frequency == "weekly":
        next_due = today + timedelta(weeks=1)
    elif frequency == "10days":
        next_due = today + timedelta(days=10)
    else:
        print("❌ Invalid frequency! Support: daily / weekly / 10days")
        return
    
    task = {
        "name": task_name,
        "type": care_type,
        "frequency": frequency,
        "last_done": None,
        "next_due": next_due
    }
    tasks.append(task)
    print(f"✅ Task added: {task_name} (Next: {next_due.strftime('%Y-%m-%d')})")

def show_tasks():
    today = datetime.date.today()
    print(f"\n📅 Today's Tasks ({today.strftime('%Y-%m-%d')})")
    today_tasks = [t for t in tasks if t["next_due"] == today]
    soon_tasks = [t for t in tasks if today < t["next_due"] <= today + timedelta(days=3)]
    
    if today_tasks:
        print("🚨 Need to do today:")
        for i, task in enumerate(today_tasks, 1):
            print(f"  {i}. {task['name']} ({CARE_GUIDES[task['type']]['name']})")
    else:
        print("  No tasks for today!")
    
    if soon_tasks:
        print("\n⚠️ Due in 3 days:")
        for i, task in enumerate(soon_tasks, 1):
            print(f"  {i}. {task['name']} (Due: {task['next_due'].strftime('%Y-%m-%d')})")

def complete_task(task_index):
    try:
        task = tasks[task_index - 1]
        today = datetime.date.today()
        task["last_done"] = today
        if task["frequency"] == "daily":
            task["next_due"] = today + timedelta(days=1)
        elif task["frequency"] == "weekly":
            task["next_due"] = today + timedelta(weeks=1)
        elif task["frequency"] == "10days":
            task["next_due"] = today + timedelta(days=10)
        print(f"✅ Task completed! Next run: {task['next_due'].strftime('%Y-%m-%d')}")
    except IndexError:
        print("❌ Invalid task number!")

def generate_travel_list(travel_days, caregiver_name, emergency_contact):
    today = datetime.date.today()
    end_date = today + timedelta(days=travel_days)
    print(f"\n📤 Travel Care Checklist ({today.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')})")
    print(f"Caregiver: {caregiver_name} | Emergency Contact: {emergency_contact}")
    print("="*60)
    
    dog_tasks = [t for t in tasks if t["type"] == "dog"]
    cat_tasks = [t for t in tasks if t["type"] == "cat"]
    succulent_tasks = [t for t in tasks if t["type"] == "succulent"]
    
    if dog_tasks:
        print("\n🐶 Dog Care")
        print(f"Basic Rules: {CARE_GUIDES['dog']['feeding']}")
        print("Tasks:")
        for task in dog_tasks:
            freq_show = task['frequency'].replace('daily', 'day').replace('weekly', 'week').replace('10days', '10 days')
            print(f"  - {task['name']}: Every {freq_show}")
    
    if cat_tasks:
        print("\n🐱 Cat Care")
        print(f"Basic Rules: {CARE_GUIDES['cat']['feeding']}")
        print("Tasks:")
        for task in cat_tasks:
            freq_show = task['frequency'].replace('daily', 'day').replace('weekly', 'week').replace('10days', '10 days')
            print(f"  - {task['name']}: Every {freq_show}")
    
    if succulent_tasks:
        print("\n🌵 Succulent Care")
        print(f"Basic Rules: {CARE_GUIDES['succulent']['watering']}")
        print("Tasks:")
        for task in succulent_tasks:
            freq_show = task['frequency'].replace('daily', 'day').replace('weekly', 'week').replace('10days', '10 days')
            print(f"  - {task['name']}: Every {freq_show}")
    
    print("\n⚠️ Important Reminders:")
    print("1. Follow the frequency strictly (no over/under care)")
    print("2. Contact emergency contact if any abnormality occurs")
    print("="*60)

# ===================== Main Interface =====================
def main():
    print("🎉 Pet & Plant Care Tool (Dog/Cat/Succulent)")
    print("="*50)
    
    while True:
        print("\nMenu:")
        print("1. View Care Guide")
        print("2. Add Care Task")
        print("3. View To-Do Tasks")
        print("4. Mark Task as Completed")
        print("5. Generate Travel Care Checklist")
        print("0. Exit")
        
        choice = input("\nPlease enter your choice (0-5): ")
        
        if choice == "1":
            care_type = input("Enter type (dog/cat/succulent): ").lower()
            show_care_guide(care_type)
        
        elif choice == "2":
            task_name = input("Enter task name (e.g.: Feed dog): ")
            care_type = input("Enter type (dog/cat/succulent): ").lower()
            if care_type not in CARE_GUIDES:
                print("❌ Invalid type!")
                continue
            if care_type == "succulent":
                frequency = input("Enter frequency (daily/weekly/10days): ").lower()
            else:
                frequency = input("Enter frequency (daily/weekly): ").lower()
            add_task(task_name, care_type, frequency)
        
        elif choice == "3":
            show_tasks()
        
        elif choice == "4":
            show_tasks()
            if tasks:
                task_num = input("\nEnter task number to complete: ")
                if task_num.isdigit():
                    complete_task(int(task_num))
                else:
                    print("❌ Please enter a number!")
        
        elif choice == "5":
            travel_days = input("Enter travel days: ")
            if not travel_days.isdigit():
                print("❌ Please enter a number!")
                continue
            caregiver = input("Enter caregiver name: ")
            emergency = input("Enter emergency contact (Name + Phone): ")
            generate_travel_list(int(travel_days), caregiver, emergency)
        
        elif choice == "0":
            print("\n👋 Goodbye! Wish your pets/plants healthy!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 0-5.")

if __name__ == "__main__":
    main()