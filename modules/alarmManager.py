"""
Alarm Manager Module - Handles CRUD operations for alarms
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class AlarmManager:
    def __init__(self, db_path: str = "database/alarms.json", history_path: str = "database/history.json"):
        self.db_path = db_path
        self.history_path = history_path
        self._ensure_directories()
        self._ensure_files()
    
    def _ensure_directories(self):
        """Ensure database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
    
    def _ensure_files(self):
        """Ensure JSON files exist"""
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump([], f)
        if not os.path.exists(self.history_path):
            with open(self.history_path, 'w') as f:
                json.dump([], f)
    
    def _load_alarms(self) -> List[Dict]:
        """Load alarms from JSON file"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_alarms(self, alarms: List[Dict]):
        """Save alarms to JSON file"""
        with open(self.db_path, 'w') as f:
            json.dump(alarms, f, indent=2)
    
    def _load_history(self) -> List[Dict]:
        """Load alarm history from JSON file"""
        try:
            with open(self.history_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_history(self, history: List[Dict]):
        """Save alarm history to JSON file"""
        with open(self.history_path, 'w') as f:
            json.dump(history, f, indent=2)
    
    def create_alarm(self, hour: int, minute: int, second: int, period: str, note: str) -> Dict:
        """Create a new alarm"""
        alarms = self._load_alarms()
        
        # Convert to 24-hour format
        hour_24 = hour if period == "AM" and hour != 12 else (hour + 12 if period == "PM" and hour != 12 else (0 if hour == 12 and period == "AM" else 12))
        
        # Generate new ID
        new_id = max([a.get('id', 0) for a in alarms], default=0) + 1
        
        alarm = {
            'id': new_id,
            'hour': hour_24,
            'minute': minute,
            'second': second,
            'period': period,
            'hour_12': hour,
            'note': note,
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        
        alarms.append(alarm)
        self._save_alarms(alarms)
        return alarm
    
    def read_alarms(self) -> List[Dict]:
        """Read all active alarms"""
        alarms = self._load_alarms()
        return [a for a in alarms if a.get('active', True)]
    
    def read_all_alarms(self) -> List[Dict]:
        """Read all alarms including inactive ones"""
        return self._load_alarms()
    
    def update_alarm(self, alarm_id: int, hour: int = None, minute: int = None, 
                     second: int = None, period: str = None, note: str = None) -> Optional[Dict]:
        """Update an existing alarm"""
        alarms = self._load_alarms()
        
        for alarm in alarms:
            if alarm['id'] == alarm_id:
                if hour is not None:
                    alarm['hour_12'] = hour
                    # Convert to 24-hour format
                    hour_24 = hour if period == "AM" and hour != 12 else (hour + 12 if period == "PM" and hour != 12 else (0 if hour == 12 and period == "AM" else 12))
                    alarm['hour'] = hour_24
                if minute is not None:
                    alarm['minute'] = minute
                if second is not None:
                    alarm['second'] = second
                if period is not None:
                    alarm['period'] = period
                    # Recalculate 24-hour format if period changed
                    if hour is not None:
                        hour_24 = alarm['hour_12'] if period == "AM" and alarm['hour_12'] != 12 else (alarm['hour_12'] + 12 if period == "PM" and alarm['hour_12'] != 12 else (0 if alarm['hour_12'] == 12 and period == "AM" else 12))
                        alarm['hour'] = hour_24
                if note is not None:
                    alarm['note'] = note
                
                self._save_alarms(alarms)
                return alarm
        
        return None
    
    def delete_alarm(self, alarm_id: int) -> bool:
        """Delete an alarm (move to history)"""
        alarms = self._load_alarms()
        history = self._load_history()
        
        for i, alarm in enumerate(alarms):
            if alarm['id'] == alarm_id:
                # Add to history
                alarm_copy = alarm.copy()
                alarm_copy['deleted_at'] = datetime.now().isoformat()
                history.append(alarm_copy)
                
                # Remove from active alarms
                alarms.pop(i)
                self._save_alarms(alarms)
                self._save_history(history)
                return True
        
        return False
    
    def get_history(self) -> List[Dict]:
        """Get alarm history"""
        return self._load_history()
    
    def get_alarm_by_id(self, alarm_id: int) -> Optional[Dict]:
        """Get a specific alarm by ID"""
        alarms = self._load_alarms()
        for alarm in alarms:
            if alarm['id'] == alarm_id:
                return alarm
        return None
    
    def format_alarm_time(self, alarm: Dict) -> str:
        """Format alarm time for display"""
        hour_12 = alarm.get('hour_12', alarm.get('hour', 0))
        minute = alarm.get('minute', 0)
        period = alarm.get('period', 'AM')
        
        return f"{hour_12:02d}:{minute:02d} {period}"

