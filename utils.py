"Helpers for Foodie Friend app."

from flask import session
from datetime import datetime
import crud

STATES = {"AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona", "CA": "California", 
          "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", 
          "HI": "Hawaii", "IA": "Iowa", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", 
          "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts", "MD": "Maryland", 
          "ME": "Maine", "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri", "MS": "Mississippi", 
          "MT": "Montana", "NC": "North Carolina", "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire", 
          "NJ": "New Jersey", "NM": "New Mexico", "NV": "Nevada", "NY": "New York", "OH": "Ohio",
          "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", 
          "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VA": "Virginia", 
          "VT": "Vermont", "WA": "Washington", "WI": "Wisconsin", "WV": "West Virginia", "WY": "Wyoming"}

def convert_time_string(time_str):
    """Convert and return time as 12-Hour Format."""

    time_12_hr = datetime.strptime(time_str, "%H%M")
    return time_12_hr.strftime("%I:%M %p")

def clean_business_hours(yelp_business_hours):
    """Clean and return dictionary of business hours."""

    if yelp_business_hours is None:
        return {}

    cleaned_business_hours = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }

    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    open_hours_dict = yelp_business_hours[0]["open"]

    for day in open_hours_dict:
        day_idx = day["day"]
        start_time = convert_time_string(day["start"])
        end_time = convert_time_string(day["end"])
        
        cleaned_business_hours[week_days[day_idx]].append(f"{start_time} - {end_time}")
    
    return cleaned_business_hours

def is_logged_in():
    """Return user or None depending on whether user is in session."""

    if "user" in session:
        return crud.get_user_by_email(session["user"])
    else:
        return None