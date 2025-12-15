"""
Sound Player Module - Handles alarm sound playback
"""
import os
import sys
import platform

def play_alarm_sound():
    """Play alarm sound notification"""
    try:
        # Try to use system beep or notification sound
        system = platform.system()
        
        if system == "Windows":
            # Windows beep
            import winsound
            winsound.Beep(1000, 500)  # Frequency 1000Hz, duration 500ms
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        elif system == "Darwin":  # macOS
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        elif system == "Linux":
            os.system('paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga 2>/dev/null || echo -e "\a"')
        else:
            # Fallback: print bell character
            print('\a')
    except Exception as e:
        # Fallback: print bell character
        print('\a')
        print(f"Could not play sound: {e}")
