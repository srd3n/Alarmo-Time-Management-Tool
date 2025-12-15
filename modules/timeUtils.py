"""
Time Utilities Module - Handles time checking and alarm triggering
"""
from datetime import datetime
from typing import List, Dict

class TimeChecker:
    def __init__(self):
        self.triggered_alarms = set()
    
    def check_alarms(self, alarms: List[Dict]) -> List[Dict]:
        """Check if any alarms should be triggered"""
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        current_second = current_time.second
        
        triggered = []
        
        for alarm in alarms:
            if not alarm.get('active', True):
                continue
            
            alarm_id = alarm.get('id')
            alarm_hour = alarm.get('hour', 0)
            alarm_minute = alarm.get('minute', 0)
            alarm_second = alarm.get('second', 0)
            
            # Check if alarm time matches current time
            if (current_hour == alarm_hour and 
                current_minute == alarm_minute and 
                current_second == alarm_second):
                
                # Only trigger if not already triggered in this second
                if alarm_id not in self.triggered_alarms:
                    triggered.append(alarm)
                    self.triggered_alarms.add(alarm_id)
            else:
                # Remove from triggered set if time has passed
                if alarm_id in self.triggered_alarms:
                    self.triggered_alarms.discard(alarm_id)
        
        return triggered

