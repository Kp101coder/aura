# import os
# import pickle
# from tkcalendar.calendar_ import Calendar as calender
# import customtkinter as ctk
# from tkinter import ttk, Text, messagebox, StringVar
# import tkinter as tk
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from datetime import datetime, timedelta, timezone
# import pytz  # For timezone support
# from PIL import Image  # Import for handling images
# from threading import Thread
# import time
# from plyer import notification  # For cross-platform notifications

# # Set up Google Calendar API
# SCOPES = ['https://www.googleapis.com/auth/calendar']
# TOKEN_FILE = 'token.pickle'

# def get_google_calendar_service():
#     creds = None
#     if os.path.exists(TOKEN_FILE):
#         with open(TOKEN_FILE, 'rb') as token:
#             creds = pickle.load(token)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_config({
#                 "installed": {
#                     "client_id": "437972213285-7nfkfeujsg5f1p9471lfc7okokpuka4d",
#                     "project_id": "aura-428720",
#                     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                     "token_uri": "https://oauth2.googleapis.com/token",
#                     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#                     "client_secret": "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",
#                     "redirect_uris": [
#                         "http://localhost"
#                     ]
#                 }
#             }, SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open(TOKEN_FILE, 'wb') as token:
#             pickle.dump(creds, token)
#     return build('calendar', 'v3', credentials=creds)

# service = get_google_calendar_service()

# def get_events():
#     print("Fetching events from Google Calendar")
#     events_result = service.events().list(calendarId='primary',
#                                           maxResults=2500, singleEvents=True,
#                                           orderBy='startTime').execute()
#     events = events_result.get('items', [])
#     print(f"Fetched {len(events)} events from Google Calendar")
#     return events

# def add_event(summary, description, start_datetime, end_datetime, location, timezone):
#     event = {
#         'summary': summary,
#         'description': description,
#         'start': {
#             'dateTime': start_datetime.isoformat(),
#             'timeZone': timezone,
#         },
#         'end': {
#             'dateTime': end_datetime.isoformat(),
#             'timeZone': timezone,
#         },
#         'location': location
#     }
#     print(f"Adding event: {event}")
#     try:
#         added_event = service.events().insert(calendarId='primary', body=event).execute()
#         print(f"Event added: {added_event.get('htmlLink')}")
#         return added_event
#     except Exception as e:
#         print(f"Error adding event: {e}")
#         return None

# def delete_event(event_id):
#     print(f"Deleting event with ID: {event_id}")
#     try:
#         service.events().delete(calendarId='primary', eventId=event_id).execute()
#         print(f"Event deleted: {event_id}")
#     except Exception as e:
#         print(f"Error deleting event: {e}")

# def update_event(event_id, summary, description, start_datetime, end_datetime, location, timezone):
#     try:
#         event = service.events().get(calendarId='primary', eventId=event_id).execute()
#         event['summary'] = summary
#         event['description'] = description
#         event['start'] = {'dateTime': start_datetime.isoformat(), 'timeZone': timezone}
#         event['end'] = {'dateTime': end_datetime.isoformat(), 'timeZone': timezone}
#         event['location'] = location
#         updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
#         print(f"Event updated: {updated_event.get('htmlLink')}")
#         return updated_event
#     except Exception as e:
#         print(f"Error updating event: {e}")
#         return None

# class CalendarApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Google Calendar Dashboard")
#         self.geometry("1024x600")
#         self.configure(bg='#2E2E2E')
#         self.events_by_date = {}  # Initialize events_by_date
#         self.selected_date = None  # Initialize selected_date
#         self.selected_tag_id = None  # Initialize selected_tag_id
#         self.notif_time = StringVar(value="30 minutes")  # Default notification lead time
#         self.create_widgets()
#         self.load_events()
#         self.select_current_date()  # Select current date and display its events
#         self.show_daily_notification()
#         self.start_notification_thread()

#     def create_widgets(self):
#         frame = ctk.CTkFrame(self)
#         frame.pack(fill="both", padx=10, pady=10, expand=True, side='left')

#         self.style = ttk.Style(self)
#         self.style.theme_use("default")

#         # Set up combobox font size
#         self.style.configure('TCombobox', font=('Helvetica', 12))

#         self.cal = calender(frame, selectmode='day', locale='en_US', disabledforeground='red',
#                               cursor="hand2", firstweekday='sunday',
#                               background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
#                               selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
#         self.cal.pack(fill="both", expand=True, padx=10, pady=10)

#         # Highlight today's date with an orange border
#         self.cal.tag_config('current_date', background='orange', foreground='white')
#         self.cal.tag_config('selected_date', background='blue', foreground='white')

#         self.cal.bind("<<CalendarSelected>>", self.display_events_for_selected_day)

#         self.create_event_controls(frame)

#         # Create a frame for displaying events on the right side
#         self.events_frame = ctk.CTkFrame(self, width=300)
#         self.events_frame.pack(fill="both", padx=10, pady=10, expand=True, side='right')
#         self.events_label = ctk.CTkLabel(self.events_frame, text="Events for selected day:", font=("Helvetica", 16))
#         self.events_label.pack(pady=10)
#         self.events_container = ctk.CTkFrame(self.events_frame)
#         self.events_container.pack(fill="both", expand=True)

#     def get_gear_icon(self):
#         gear_image = Image.open("gear_icon.png")
#         gear_image = gear_image.resize((20, 20), Image.Resampling.LANCZOS)
#         gear_icon = ctk.CTkImage(light_image=gear_image, dark_image=gear_image, size=(20, 20))
#         return gear_icon

#     def create_event_controls(self, parent):
#         controls_frame = ctk.CTkFrame(parent)
#         controls_frame.pack(fill="x", padx=10, pady=10)

#         add_button = ctk.CTkButton(controls_frame, text="Add Event", command=self.add_event_prompt)
#         add_button.pack(side='left', padx=10)

#         self.remove_button = ctk.CTkButton(controls_frame, text="Remove Event", command=self.confirm_remove_event, state='disabled')
#         self.remove_button.pack(side='left', padx=10)

#         self.edit_button = ctk.CTkButton(controls_frame, text="Edit Event", command=self.edit_event, state='disabled')
#         self.edit_button.pack(side='left', padx=10)

#         self.settings_button = ctk.CTkButton(controls_frame, text="", image=self.get_gear_icon(), command=self.open_settings)
#         self.settings_button.pack(side='left', padx=10)

#     def display_events_for_selected_day(self, event):
#         selected_date = self.cal.selection_get()
#         if selected_date:
#             if self.selected_tag_id:
#                 self.cal.calevent_remove(self.selected_tag_id)
#             self.selected_date = selected_date
#             self.selected_tag_id = self.cal.calevent_create(selected_date, '', 'selected_date')
#             self.display_events_for_day(selected_date.strftime('%Y-%m-%d'))
#         self.cal.selection_clear()

#     def display_events_for_day(self, date_str):
#         print(f"Displaying events for {date_str}")
#         for widget in self.events_container.winfo_children():
#             widget.destroy()

#         self.selected_event = None
#         self.remove_button.configure(state='disabled')
#         self.edit_button.configure(state='disabled')

#         if date_str in self.events_by_date:
#             for event in self.events_by_date[date_str]:
#                 start_time = event['start'].get('dateTime')
#                 end_time = event['end'].get('dateTime')
#                 start = datetime.fromisoformat(start_time).strftime('%I:%M %p') if start_time else ''
#                 end = datetime.fromisoformat(end_time).strftime('%I:%M %p') if end_time else ''
#                 summary = event.get('summary', 'Untitled')
#                 location = event.get('location', '')
#                 description = event.get('description', '')

#                 event_details = f"{start} - {end}\n{summary}\n{location}\n{description}"
#                 event_button = ctk.CTkButton(self.events_container, text=event_details, command=lambda e=event: self.set_selected_event(e))
#                 event_button.pack(fill="x", padx=5, pady=5)
#         else:
#             no_event_label = ctk.CTkLabel(self.events_container, text="No events for this day.", font=("Helvetica", 12))
#             no_event_label.pack(pady=10)

#     def set_selected_event(self, event):
#         self.selected_event = event
#         self.remove_button.configure(state='normal')
#         self.edit_button.configure(state='normal')

#     def load_events(self):
#         events = get_events()
#         self.update_calendar_events(events)

#     def update_calendar_events(self, events):
#         self.events_by_date = {}

#         for event in events:
#             start = event['start'].get('dateTime', event['start'].get('date'))
#             date_str = start.split("T")[0]
#             if date_str not in self.events_by_date:
#                 self.events_by_date[date_str] = []
#             self.events_by_date[date_str].append(event)
#         self.refresh_calendar()

#     def refresh_calendar(self):
#         self.cal.calevent_remove('all')
#         today = datetime.today().date()
#         self.cal.calevent_create(today, '', 'current_date')
#         for date_str, events in self.events_by_date.items():
#             for event in events:
#                 summary = event.get('summary', 'Untitled')
#                 self.cal.calevent_create(datetime.strptime(date_str, '%Y-%m-%d'), summary, 'event')
#         self.highlight_dates_with_events()
#         if self.selected_date:
#             self.display_events_for_day(self.selected_date.strftime('%Y-%m-%d'))

#     def highlight_dates_with_events(self):
#         for date_str in self.events_by_date:
#             date = datetime.strptime(date_str, '%Y-%m-%d')
#             self.cal.calevent_create(date, '', 'event')
#         self.cal.tag_config('event', background='red', foreground='white')

#     def add_event_prompt(self):
#         selected_date = self.selected_date
#         if not selected_date:
#             print("No date selected")
#             return
#         self.event_prompt("Add Event", self.add_event_callback, selected_date=selected_date)

#     def edit_event_prompt(self):
#         self.event_prompt("Edit Event", self.edit_event_callback, self.selected_event, selected_date=self.selected_date)

#     def event_prompt(self, title, callback, event=None, selected_date=None):
#         prompt = ctk.CTkToplevel(self)
#         prompt.title(title)
#         prompt.geometry("500x700")
#         prompt.grab_set()  # Make the new window modal

#         summary_label = ctk.CTkLabel(prompt, text="Summary:")
#         summary_label.pack(pady=5)
#         summary_entry = ctk.CTkEntry(prompt, width=300)
#         summary_entry.pack(pady=5)

#         description_label = ctk.CTkLabel(prompt, text="Description:")
#         description_label.pack(pady=5)
#         description_entry = ctk.CTkEntry(prompt, width=300)
#         description_entry.pack(pady=5)

#         location_label = ctk.CTkLabel(prompt, text="Location:")
#         location_label.pack(pady=5)
#         location_entry = ctk.CTkEntry(prompt, width=300)
#         location_entry.pack(pady=5)

#         start_label = ctk.CTkLabel(prompt, text="Start Time (HH:MM):")
#         start_label.pack(pady=5)
#         start_frame = ctk.CTkFrame(prompt)
#         start_frame.pack(pady=5)
#         start_entry = ctk.CTkEntry(start_frame, width=100)
#         start_entry.pack(side="left")
#         start_ampm = ttk.Combobox(start_frame, values=["AM", "PM"], width=5, font=("Helvetica", 14))  # Increased width
#         start_ampm.set("AM")
#         start_ampm.pack(side="left")

#         end_label = ctk.CTkLabel(prompt, text="End Time (HH:MM):")
#         end_label.pack(pady=5)
#         end_frame = ctk.CTkFrame(prompt)
#         end_frame.pack(pady=5)
#         end_entry = ctk.CTkEntry(end_frame, width=100)
#         end_entry.pack(side="left")
#         end_ampm = ttk.Combobox(end_frame, values=["AM", "PM"], width=5, font=("Helvetica", 14))  # Increased width
#         end_ampm.set("AM")
#         end_ampm.pack(side="left")

#         timezone_label = ctk.CTkLabel(prompt, text="Time Zone:")
#         timezone_label.pack(pady=5)
#         timezone_combobox = ttk.Combobox(prompt, values=pytz.all_timezones, width=15, font=("Helvetica", 14))  # Increased width
#         timezone_combobox.set('UTC')
#         timezone_combobox.pack(pady=5)

#         if event:
#             summary_entry.insert(0, event.get('summary', ''))
#             description_entry.insert(0, event.get('description', ''))
#             location_entry.insert(0, event.get('location', ''))
#             start_datetime = datetime.fromisoformat(event['start']['dateTime']) if 'dateTime' in event['start'] else None
#             end_datetime = datetime.fromisoformat(event['end']['dateTime']) if 'dateTime' in event['end'] else None
#             if start_datetime:
#                 start_entry.insert(0, start_datetime.strftime('%I:%M'))
#                 start_ampm.set(start_datetime.strftime('%p'))
#             if end_datetime:
#                 end_entry.insert(0, end_datetime.strftime('%I:%M'))
#                 end_ampm.set(end_datetime.strftime('%p'))
#             timezone_combobox.set(event['start'].get('timeZone', 'UTC'))

#         confirm_button = ctk.CTkButton(prompt, text="Confirm", command=lambda: callback(
#             summary_entry.get(), description_entry.get(), location_entry.get(),
#             self.convert_to_datetime(selected_date, start_entry.get(), start_ampm.get()) if start_entry.get() else None,
#             self.convert_to_datetime(selected_date, end_entry.get(), end_ampm.get()) if end_entry.get() else None,
#             timezone_combobox.get(), event['id'] if event else None, prompt))
#         confirm_button.pack(pady=20)

#     def convert_to_datetime(self, date, time_str, ampm):
#         if date is None:
#             return None
#         time = datetime.strptime(time_str + ampm, '%I:%M%p').time()
#         return datetime.combine(date, time)

#     def add_event_callback(self, summary, description, location, start_datetime, end_datetime, timezone, _, prompt):
#         if not summary:
#             messagebox.showerror("Error", "Summary is required")
#             return
#         if start_datetime is None or end_datetime is None:
#             messagebox.showerror("Error", "Start and end times are required")
#             return
#         event = add_event(summary, description, start_datetime, end_datetime, location, timezone)
#         if event:
#             notification.notify(
#                 title="Event Added",
#                 message=f"Event '{summary}' has been added successfully.",
#                 timeout=2
#             )
#             print(f"Event added successfully: {event.get('htmlLink')}")
#         else:
#             print("Failed to add event")
#         prompt.destroy()
#         self.load_events()
#         self.display_events_for_day(self.selected_date.strftime('%Y-%m-%d'))

#     def confirm_remove_event(self):
#         if hasattr(self, 'selected_event'):
#             response = messagebox.askyesno("Confirm Remove", "Are you sure you want to remove this event?")
#             if response:
#                 self.remove_event_callback(self.selected_event['id'])

#     def remove_event_callback(self, event_id):
#         delete_event(event_id)
#         notification.notify(
#             title="Event Removed",
#             message=f"Event has been removed successfully.",
#             timeout=2
#         )
#         self.load_events()
#         self.display_events_for_day(self.selected_date.strftime('%Y-%m-%d'))

#     def edit_event(self):
#         if hasattr(self, 'selected_event'):
#             self.edit_event_prompt()

#     def edit_event_callback(self, summary, description, location, start_datetime, end_datetime, timezone, event_id, prompt):
#         if not summary:
#             messagebox.showerror("Error", "Summary is required")
#             return
#         if start_datetime is None or end_datetime is None:
#             messagebox.showerror("Error", "Start and end times are required")
#             return
#         event = update_event(event_id, summary, description, start_datetime, end_datetime, location, timezone)
#         if event:
#             notification.notify(
#                 title="Event Updated",
#                 message=f"Event '{summary}' has been updated successfully.",
#                 timeout=2
#             )
#             print(f"Event updated successfully: {event.get('htmlLink')}")
#         else:
#             print("Failed to update event")
#         prompt.destroy()
#         self.load_events()
#         self.display_events_for_day(self.selected_date.strftime('%Y-%m-%d'))

#     def select_current_date(self):
#         today = datetime.today().date()
#         self.cal.selection_set(today)
#         self.selected_date = today
#         self.selected_tag_id = self.cal.calevent_create(today, '', 'selected_date')
#         self.display_events_for_day(today.strftime('%Y-%m-%d'))

#     def open_settings(self):
#         settings_window = ctk.CTkToplevel(self)
#         settings_window.title("Settings")
#         settings_window.geometry("400x300")
#         settings_window.grab_set()  # Make the new window modal

#         settings_label = ctk.CTkLabel(settings_window, text="Settings", font=("Helvetica", 16))
#         settings_label.pack(pady=20)

#         # Notification settings
#         notif_frame = ctk.CTkFrame(settings_window)
#         notif_frame.pack(pady=10, padx=10, fill='x')

#         notif_label = ctk.CTkLabel(notif_frame, text="Notification lead time:")
#         notif_label.pack(side="left", padx=10)
        
    
#         notif_times = ["1 minute", "5 minutes", "10 minutes", "20 minutes", "30 minutes", "1 hour", "2 hours", "4 hours"]
#         notif_dropdown = ttk.Combobox(notif_frame, textvariable=self.notif_time, values=notif_times, width=20, font=("Helvetica", 14))  # Increased width
#         notif_dropdown.pack(side="left", padx=10)
#         notif_dropdown.set(self.notif_time.get())

#         confirm_button = ctk.CTkButton(settings_window, text="Confirm", command=settings_window.destroy)
#         confirm_button.pack(pady=20)

#     def show_daily_notification(self):
#         today_str = datetime.today().strftime('%Y-%m-%d')
#         if today_str in self.events_by_date:
#             num_events = len(self.events_by_date[today_str])
#             notification.notify(
#                 title="Today's Events",
#                 message=f"You have {num_events} events today.",
#                 timeout=3
#             )

#     def start_notification_thread(self):
#         self.notif_thread = Thread(target=self.check_for_notifications)
#         self.notif_thread.daemon = True
#         self.notif_thread.start()

#     def check_for_notifications(self):
#         while True:
#             now = datetime.now().astimezone()
#             for event_date, events in self.events_by_date.items():
#                 for event in events:
#                     start = event['start'].get('dateTime')
#                     start_dt = datetime.fromisoformat(start).astimezone() if start else None
#                     if start_dt:
#                         lead_time = self.get_lead_time_delta()
#                         notif_time = start_dt - lead_time
#                         if now >= notif_time and now < start_dt:
#                             notification.notify(
#                                 title="Upcoming Event",
#                                 message=f"{event['summary']} is starting soon!",
#                                 timeout=4
#                             )
#             time.sleep(60)  # Check every minute

#     def get_lead_time_delta(self):
#         lead_time_str = self.notif_time.get()
#         if "minute" in lead_time_str:
#             minutes = int(lead_time_str.split()[0])
#             return timedelta(minutes=minutes)
#         elif "hour" in lead_time_str:
#             hours = int(lead_time_str.split()[0])
#             return timedelta(hours=hours)
#         return timedelta(minutes=30)  # Default to 30 minutes

# if __name__ == "__main__":
#     app = CalendarApp()
#     app.mainloop()
