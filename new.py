import sys
import time
import pyttsx3
import datetime
import threading
from typing import Optional

# Initialize TTS engine
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('rate', 150) 
tts_engine.setProperty('volume', 0.9)

# Find a male voice if available
male_voice = None
if voices:
    for voice in voices:
        if voice.id and ('male' in voice.id.lower() or 'david' in voice.id.lower()):
            male_voice = voice
            break

if male_voice:
    tts_engine.setProperty('voice', male_voice.id)
    print("✓ MALE Voice engine initialized successfully")
else:
    if voices:  # Check if there are any voices available
        tts_engine.setProperty('voice', voices[0].id)
    print("✓ Voice engine initialized successfully")

def _get_current_time_text(now: Optional[datetime.datetime] = None) -> str:
    if now is None:
        now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    
    # Convert to 12-hour format
    if hour == 0:
        hour_12 = 12
        period = "AM"
    elif hour < 12:
        hour_12 = hour
        period = "AM"
    elif hour == 12:
        hour_12 = 12
        period = "PM"
    else:
        hour_12 = hour - 12
        period = "PM"
    
    # Format the time string
    if minute == 0:
        time_text = f"Time right now is {hour_12} {period}"
    else:
        time_text = f"Time right now is {hour_12}:{minute:02d} {period}"
    
    return time_text

def _announce_time(t='') -> None:
    try:
        if(t==''):
            time_text = _get_current_time_text()
        else:
            time_text = t
        print(f"🔊 Announcing: {time_text}")
        tts_engine.say(time_text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"❌ Error announcing time: {e}")

def _announce_now_and_next(next_dt: datetime.datetime) -> None:
    try:
        now_text = _get_current_time_text()
        next_text = f"Next announcement will be made at {next_dt.strftime('%I:%M %p')}"
        print(f"🔊 Announcing: {now_text}")
        print(f"🔄 {next_text}")
        tts_engine.say(now_text)
        tts_engine.say(next_text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"❌ Error announcing now/next: {e}")

def _start_():
    interval_input = input("Enter time interval in minutes (default: 5min): ").strip()
    interval_minutes = 5
    if interval_input:
        try:
            interval_minutes = int(interval_input)
            if interval_minutes <= 0:
                print("Interval must be positive. Using default 5 minutes.")
                interval_minutes = 5
        except ValueError:
            print("Invalid input. Using default 5 minutes.")
            interval_minutes = 5
    
    # Convert to seconds for more precise timing
    interval_seconds = interval_minutes * 60
    
    print("🎤 Voice Time Tracker")
    print("=" * 40)
    print(f"⏰ Announcement interval: {interval_minutes} minutes")
    is_running = True
    
    # Compute next announcement strictly in the future and announce now+next together
    print("\n🔊 Starting with initial announcements...")
    now = datetime.datetime.now()
    base_minute = now.replace(second=0, microsecond=0)
    remainder = base_minute.minute % interval_minutes
    minutes_to_add = (interval_minutes - remainder) % interval_minutes
    next_announcement = base_minute + datetime.timedelta(minutes=minutes_to_add)
    if next_announcement <= now:
        next_announcement += datetime.timedelta(minutes=interval_minutes)
    _announce_now_and_next(next_announcement)
    
    try:
        while is_running:
            # Calculate precise time to wait
            now = datetime.datetime.now()
            if now >= next_announcement:
                # Compute the following announcement strictly in the future
                next_announcement = next_announcement + datetime.timedelta(minutes=interval_minutes)
                next_announcement = next_announcement.replace(second=0, microsecond=0)
                while next_announcement <= now:
                    next_announcement += datetime.timedelta(minutes=interval_minutes)
                # Announce current time and the upcoming next time in one TTS run
                _announce_now_and_next(next_announcement)
            else:
                # Calculate precise sleep time
                time_to_wait = (next_announcement - now).total_seconds()
                
                # Sleep in smaller increments to allow for keyboard interrupt
                sleep_increment = min(1.0, time_to_wait)  # Sleep at most 1 second at a time
                while time_to_wait > 0 and is_running:
                    try:
                        time.sleep(sleep_increment)
                        time_to_wait -= sleep_increment
                        # Update current time to account for any drift
                        now = datetime.datetime.now()
                        if now >= next_announcement:
                            break
                    except KeyboardInterrupt:
                        print("\n🛑 Stopping Voice Time Tracker...")
                        is_running = False
                        break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping Voice Time Tracker...")
    finally:
        print("\n👋 Goodbye!")
        if tts_engine._inLoop:
            tts_engine.endLoop()

if __name__ == "__main__":
    _start_()