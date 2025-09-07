# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

VoiceTrackerTime is a Python desktop application that announces the current time at configurable intervals using text-to-speech. The application is designed primarily for Windows and uses system TTS engines to provide robotic voice announcements.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Alternative: Install in development mode
pip install -e .
```

### Running the Application
```bash
# Run the main robust version
python voice_time_tracker_scheduling.py

# Run the simpler version (with 1-minute offset announcements)
python late_by_1min.py
```

### Development Tasks
```bash
# Check for import errors without running
python -m py_compile voice_time_tracker_scheduling.py
python -m py_compile late_by_1min.py

# Basic syntax checking
python -m flake8 *.py  # If flake8 is installed
```

## Architecture & Code Structure

### Core Architecture
The application follows a class-based architecture with the main `VoiceTimeTracker` class in `voice_time_tracker_scheduling.py`:

- **VoiceTimeTracker Class**: Main application controller that manages TTS engine, scheduling, and user interaction
- **Threading Model**: Uses a separate daemon thread for the announcement loop to keep the main thread responsive
- **TTS Configuration**: Automatically detects and configures system voices, preferring male voices for more robotic sound

### Key Components

**voice_time_tracker_scheduling.py** (Robust Implementation):
- Full class-based architecture with proper error handling
- Configurable interval timing with user input validation
- Thread-safe operation with graceful shutdown handling
- Smart scheduling that aligns announcements to exact minute boundaries
- Voice engine initialization with fallback options

**late_by_1min.py** (Simple Implementation):
- Simplified procedural approach
- Announces both current time and next announcement time
- Direct time-based waiting without complex scheduling
- Less error handling but more straightforward logic

### Voice Engine Configuration
Both implementations:
1. Initialize `pyttsx3` TTS engine
2. Scan available system voices for male/robotic options
3. Configure speech rate (150 WPM) and volume (90%)
4. Format time in 12-hour format for natural speech

## Key Dependencies

- **pyttsx3**: Cross-platform text-to-speech library (primary TTS engine)
- **pywin32**: Windows-specific API access (required for TTS on Windows)
- **pygame**: Audio/multimedia library (likely for additional audio features)
- **python-dateutil**: Enhanced datetime handling utilities

## Windows-Specific Considerations

This application is primarily designed for Windows:
- Uses `pywin32` for system integration
- TTS voice detection logic specifically looks for Windows voice identifiers
- Path separators and system commands assume Windows environment
- Voice engine preferences target Windows SAPI voices

## Development Notes

- **Python Version**: Requires Python 3.11 (specified in `.python-version`)
- **No Testing Framework**: Currently no test suite exists
- **No Linting Setup**: No pre-configured linting or formatting tools
- **Voice Initialization**: Always test voice engine initialization first when debugging audio issues
- **Thread Safety**: The robust implementation uses threading - be careful with shared state modifications
- **Time Formatting**: Both implementations use custom 12-hour time formatting rather than strftime for speech clarity
