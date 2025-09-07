#!/usr/bin/env python3
"""
Voice Time Tracker
A Python application that announces the current time at configurable intervals
using a robotic voice throughout the day.
"""
import sys
import time
import pyttsx3
import datetime
import threading
from typing import Optional




class VoiceTimeTracker:
    """Main class for the voice time tracking application."""
    
    def __init__(self, interval_minutes: int = 5):
        """
        Initialize the voice time tracker.
        
        Args:
            interval_minutes (int): Time interval in minutes between announcements
        """
        self.interval_minutes = interval_minutes
        self.interval_seconds = interval_minutes * 60
        self.is_running = False
        self.tts_engine: Optional[pyttsx3.Engine] = None
        
        # Initialize text-to-speech engine
        self._setup_voice_engine()
    
    def _setup_voice_engine(self) -> None:
        """Setup and configure the text-to-speech engine with robotic voice."""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            
            # Configure voice properties for robotic sound
            self.tts_engine.setProperty('rate', 150)    # Slower speech rate
            self.tts_engine.setProperty('volume', 0.9)  # High volume
            
            # Try to set a more robotic-sounding voice (usually male voices sound more robotic)
            if voices:
                # Prefer male voices for more robotic sound
                male_voice = None
                for voice in voices:
                    if voice.id and ('male' in voice.id.lower() or 'david' in voice.id.lower()):
                        male_voice = voice
                        break
                
                if male_voice:
                    self.tts_engine.setProperty('voice', male_voice.id)
                else:
                    # Use first available voice if no male voice found
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            print("✓ Voice engine initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing voice engine: {e}")
            sys.exit(1)
    
    def _get_current_time_text(self) -> str:
        """
        Get the current time formatted for speech.
        
        Returns:
            str: Formatted time string for TTS
        """
        now = datetime.datetime.now()
        
        # Format time for natural speech
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
        
        # Format the announcement
        if minute == 0:
            time_text = f"Time right now is {hour_12} {period}"
        else:
            time_text = f"Time right now is {hour_12}:{minute:02d} {period}"
        
        return time_text
    
    def _announce_time(self) -> None:
        """Announce the current time using text-to-speech."""
        try:
            time_text = self._get_current_time_text()
            print(f"🔊 Announcing: {time_text}")
            
            if self.tts_engine:
                self.tts_engine.say(time_text)
                self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"❌ Error announcing time: {e}")
    
    def _run_tracker(self) -> None:
        """Main tracking loop that runs in a separate thread."""
        print(f"⏰ Voice Time Tracker started (interval: {self.interval_minutes} minutes)")
        print("Press Ctrl+C to stop")

        # Announce immediately
        self._announce_time()
        next_announcement = datetime.datetime.now() + datetime.timedelta(minutes=self.interval_minutes)
        next_announcement = next_announcement.replace(second=0, microsecond=0)

        while self.is_running:
            try:
                now = datetime.datetime.now()
                if now >= next_announcement:
                    self._announce_time()
                    # schedule next announcement
                    next_announcement = now + datetime.timedelta(minutes=self.interval_minutes)
                    next_announcement = next_announcement.replace(second=0, microsecond=0)
                    print(f"🔄 Next announcement at: {next_announcement.strftime('%I:%M %p')}")

                # small sleep to avoid busy CPU
                time.sleep(1)

            except KeyboardInterrupt:
                print("\n🛑 Stopping Voice Time Tracker...")
                self.is_running = False
                break
            except Exception as e:
                print(f"❌ Error in tracking loop: {e}")
                time.sleep(2)
    
    def start(self) -> None:
        """Start the voice time tracker."""
        if self.is_running:
            print("⚠️  Voice Time Tracker is already running!")
            return
        
        self.is_running = True
        
        # Start the tracking in a separate thread
        tracker_thread = threading.Thread(target=self._run_tracker, daemon=True)
        tracker_thread.start()
        
        try:
            # Keep the main thread alive
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the voice time tracker."""
        self.is_running = False
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass
        print("✅ Voice Time Tracker stopped")


def main():
    """Main function to run the Voice Time Tracker."""
    print("🎤 Voice Time Tracker")
    print("=" * 40)
    
    # Get user configuration
    try:
        interval = input("Enter time interval in minutes (default: 5): ").strip()
        if interval:
            interval_minutes = int(interval)
            if interval_minutes <= 0:
                raise ValueError("Interval must be positive")
        else:
            interval_minutes = 5
            
    except ValueError as e:
        print(f"❌ Invalid interval: {e}")
        print("Using default interval of 5 minutes")
        interval_minutes = 5
    
    # Create and start the tracker
    tracker = VoiceTimeTracker(interval_minutes=interval_minutes)
    
    try:
        tracker.start()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        tracker.stop()


if __name__ == "__main__":
    main()
