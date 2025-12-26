import json
import os
from datetime import datetime, date

DATA_FILE = "user_data.json"

def load_stats():
    """Loads user stats from JSON file or returns default."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass # Return default if error
            
    return {
        "total_seconds": 0,
        "current_streak": 0,
        "last_study_date": None,
        "reminders_enabled": False,
        "xp": 0,
        "level": 1,
        "weekly_activity": {
            "Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0
        },
        "tasks": []
    }

def save_stats(stats):
    """Saves stats to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(stats, f, indent=4)

def add_xp(amount):
    """Adds XP and handles leveling up. Returns (new_xp, new_level, leveled_up_bool)"""
    stats = load_stats()
    
    # Ensure keys exist for old save files
    if "xp" not in stats: stats["xp"] = 0
    if "level" not in stats: stats["level"] = 1
    
    stats["xp"] += amount
    current_level = stats["level"]
    xp_needed = current_level * 100 # Simple scaling: Lv1=100, Lv2=200, etc.
    
    leveled_up = False
    if stats["xp"] >= xp_needed:
        stats["xp"] -= xp_needed # Reset XP or Carry over (Carry over is better typically, but reset is simpler for bar)
        # Let's do partial reset: XP serves as progress to next level only?
        # Standard RPG: XP accumulates total? Or XP resets per level?
        # Simplest UI: XP is "Current progress".
        # Let's keep XP as "Progress to next level" for simple visualization
        stats["level"] += 1
        leveled_up = True
    
    save_stats(stats)
    return stats["xp"], stats["level"], leveled_up

def update_streak(stats):
    """Updates streak logic based on dates."""
    today_str = str(date.today())
    last_date = stats.get("last_study_date")
    
    if last_date == today_str:
        return stats # Already studied today
        
    # Check if yesterday was studied
    if last_date:
        last_dt = datetime.strptime(last_date, "%Y-%m-%d").date()
        delta = (date.today() - last_dt).days
        
        if delta == 1:
            stats["current_streak"] += 1
        else:
            stats["current_streak"] = 1 # Reset streak
    else:
        stats["current_streak"] = 1 # First time
        
    stats["last_study_date"] = today_str
    return stats

def add_study_time(seconds):
    """updates total time and saves."""
    stats = load_stats()
    stats["total_seconds"] += seconds
    
    # Update Weekly Activity (Simple Mock logic for now, just adding to today)
    today_name = date.today().strftime("%a")
    if "weekly_activity" not in stats:
        stats["weekly_activity"] = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
        
    current_val = stats["weekly_activity"].get(today_name, 0)
    stats["weekly_activity"][today_name] = current_val + (seconds / 60) # Store minutes
    
    stats = update_streak(stats)
    save_stats(stats)
    return stats

# --- TASK MANAGER HELPERS ---
def add_task(text, priority):
    stats = load_stats()
    if "tasks" not in stats:
        stats["tasks"] = []
    
    stats["tasks"].append({
        "text": text,
        "priority": priority, # High, Medium, Low
        "done": False,
        "created_at": str(datetime.now())
    })
    save_stats(stats)

def toggle_task(index):
    stats = load_stats()
    if 0 <= index < len(stats["tasks"]):
        stats["tasks"][index]["done"] = not stats["tasks"][index]["done"]
        save_stats(stats)

def delete_task(index):
    stats = load_stats()
    if 0 <= index < len(stats["tasks"]):
        stats["tasks"].pop(index)
        save_stats(stats)
