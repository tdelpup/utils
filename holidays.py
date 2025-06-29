import calendar
import datetime
from datetime import date
from dateutil import relativedelta

class HolidayCalendar(calendar.TextCalendar):
    def __init__(self, holidays, current_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.holidays = set(holidays)
        self.current_date = current_date

    def formatday(self, day, weekday, width):
        if day == 0:
            s = ' ' * width
        else:
            date_obj = datetime.date(self.year, self.month, day)
            day_str = str(day).rjust(width)
            
            if date_obj == self.current_date:
                s = f"\033[47m\033[1m\033[30m{day_str}\033[0m"
            elif date_obj in self.holidays:
                s = f"\033[1m\033[91m{day_str}\033[0m"
            else:
                s = day_str
        return s
    
    def formatmonthname(self, theyear, themonth, width, withyear=True):
        """Return a formatted month name with bold formatting."""
        names = []
        if withyear:
            names.append(calendar.month_name[themonth])
            names.append(str(theyear))
        else:
            names.append(calendar.month_name[themonth])
        
        month_name = ' '.join(names)
        return f"\033[1m{month_name.center(width).rstrip()}\033[0m"
    
    def formatmonth(self, theyear, themonth, w=0, l=0):
        self.year = theyear
        self.month = themonth
        return super().formatmonth(theyear, themonth, w, l)

current_date = date.today()
current_year = current_date.year
current_month = current_date.month

next_date = current_date + relativedelta.relativedelta(months=1)
next_year = next_date.year
next_month = next_date.month

hols = {
    "USA": [date(2025, 7, 4), date(2025, 6, 29)],
    "ARG": [date(2025, 6, 25), date(2025, 6, 30)],
    "ARG2": [date(2025, 6, 25), date(2025, 6, 30)],
    "ARG3": [date(2025, 6, 25), date(2025, 6, 30)],
    "ARG4": [date(2025, 6, 25), date(2025, 6, 30)],
    "ARG5": [date(2025, 6, 25), date(2025, 6, 30)],
    "ARG6": [date(2025, 6, 25), date(2025, 6, 30)],
    "ARG7": [date(2025, 6, 25), date(2025, 6, 30)]
}

def get_days_until_next_holiday(holidays, country):
    """Calculate days until the next holiday for a given country"""
    if country not in holidays:
        return None
    
    all_holidays = holidays[country]
    future_holidays = [h for h in all_holidays if h >= current_date]
    
    if not future_holidays:
        return None
    
    next_holiday = min(future_holidays)
    days_until = (next_holiday - current_date).days
    
    return days_until, next_holiday

def get_calendar_lines(holidays, country, year, month):
    """Get calendar as list of lines for a given country, year, and month"""
    if country not in holidays:
        return [f"No holiday data for {country}"]
    
    country_holidays = [h for h in holidays[country] if h.year == year and h.month == month]
    cal = HolidayCalendar(country_holidays, current_date, firstweekday=6)
    calendar_str = cal.formatmonth(year, month)
    return calendar_str.split('\n')

def print_calendars_by_country(holidays):
    """Print calendars with months (Y axis), countries (X axis)"""
    country_calendars = {}
    max_visual_width = 0
    
    countries = list(holidays.keys())
    for country in countries:
        current_lines = get_calendar_lines(holidays, country, current_year, current_month)
        next_lines = get_calendar_lines(holidays, country, next_year, next_month)
        
        combined_lines = []
        
        header = f"{country}".center(20)
        combined_lines.append(header)
        combined_lines.append("=" * 20)
        
        holiday_info = get_days_until_next_holiday(holidays, country)
        if holiday_info:
            days_until, _ = holiday_info
            if days_until == 0:
                holiday_text = "Holiday today!"
            elif days_until == 1:
                holiday_text = "Holiday tomorrow!"
            else:
                holiday_text = f"{days_until} days to holiday"
            combined_lines.append(holiday_text.center(20))
        else:
            combined_lines.append("No upcoming holidays".center(20))
        
        combined_lines.append("-" * 20)
        combined_lines.extend(current_lines)
        combined_lines.extend(next_lines)
        country_calendars[country] = combined_lines
        
        for line in combined_lines:
            visual_line = line.replace('\033[91m', '').replace('\033[0m', '').replace('\033[47m', '').replace('\033[30m', '').replace('\033[1m', '')
            max_visual_width = max(max_visual_width, len(visual_line))
    
    max_lines = max(len(lines) for lines in country_calendars.values())
    
    for line_idx in range(max_lines):
        output_line = ""
        for i, country in enumerate(countries):
            if i > 0:
                output_line += "    "
            
            lines = country_calendars[country]
            if line_idx < len(lines):
                line = lines[line_idx]
                visual_line = line.replace('\033[91m', '').replace('\033[0m', '').replace('\033[47m', '').replace('\033[30m', '').replace('\033[1m', '')
                padding_needed = max_visual_width - len(visual_line)
                line = line + " " * padding_needed
            else:
                line = " " * max_visual_width
            
            output_line += line
        print(output_line)

print_calendars_by_country(hols)