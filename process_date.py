import datetime
import calendar

# Current date
current_date = datetime.datetime.now()
print("current_date:", current_date)

# Extract month and year
month = current_date.month
year = current_date.year
print("month:", month)
print("year:", year)

print("current_date.day:", current_date.day)

# Adjust month and year based on the date <= 5
if current_date.day <= 5:
    month -= 2
    if month <= 0:  # If the adjusted month is zero or negative, set the year
        month += 12
        year -= 1
else:
    month -= 1
    if month <= 0:  # If the adjusted month is zero or negative, set the year
        month += 12
        year -= 1

print("month_New:", month)
print("year_New:", year)

# Get the previous month
prev_month_date = datetime.date(year, month, 1)
prev_mon_name_MM = prev_month_date.strftime('%B')
prev_mon_name_mm = prev_month_date.strftime('%b')

print("prev_mon_name_MM:", prev_mon_name_MM)
print("prev_mon_name_mm:", prev_mon_name_mm)

# Year
current_year_yyyy = year

# Format the year to 2 digits
current_year_yy = year % 100

print("current_year_yy:", current_year_yy)

# Get the number of days in the previous month
days_in_mon = calendar.monthrange(year, month)[1]

dt = "th"
# Format the number of days
if days_in_mon in [30, 28, 29]:
    dt = "th"
elif days_in_mon == 31:
    dt = "st"

days_in_month = str(days_in_mon) + dt

print("days_in_month_formatted:", days_in_month)
