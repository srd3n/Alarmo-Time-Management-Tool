# Alarmo - Time Management Tool

A desktop alarm application built with Python and Tkinter that provides CRUD (Create, Read, Update, Delete) functionality for managing alarms.

## Features

- **Create Alarms**: Set alarms with hour, minute, second, AM/PM period, and custom notes
- **View Alarms**: Display all active alarms in a scrollable list
- **Update Alarms**: Modify existing alarms by selecting them and updating the fields
- **Delete Alarms**: Remove alarms (moved to history)
- **History**: View deleted alarms history
- **Real-time Alarm Checking**: Background thread checks and triggers alarms at the specified time
- **Sound Notifications**: Plays system sounds when alarms trigger

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed
3. No additional packages required (uses built-in libraries)

## Usage

Run the application:

```bash
python main.py
```

### Adding an Alarm

1. Enter the hour (1-12), minute (0-59), and second (0-59)
2. Select AM or PM
3. Optionally add a note describing the alarm
4. Click "ADD ALARM"

### Updating an Alarm

1. Select an alarm from the list (it will be highlighted)
2. Modify the time fields and/or note
3. Click "UPDATE"

### Deleting an Alarm

1. Select an alarm from the list
2. Click "DELETE"
3. Confirm the deletion

### Viewing History

Click the "HISTORY" button to view all previously deleted alarms.

## Data Storage

- Active alarms are stored in `database/alarms.json`
- Alarm history is stored in `database/history.json`

## GUI Layout

The application features a two-panel layout:
- **Left Panel**: Alarm creation form with time inputs and note field
- **Right Panel**: Active alarms list with action buttons (DELETE, UPDATE, HISTORY)

## Notes

- Alarms are checked every second in the background
- When an alarm triggers, a system sound plays and a notification dialog appears
- The application uses 12-hour format with AM/PM for user input but stores times in 24-hour format internally

