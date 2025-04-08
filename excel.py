import xlsxwriter
import random

# Create workbook and worksheet
workbook = xlsxwriter.Workbook('Cricket Coaching.xlsx')
worksheet = workbook.add_worksheet('firstsheet')

headers = ['Name', 'Date of Join', 'Attendance', 'Practice Hour', 'Month', 'Practice date', 'Session Type', 'Coach', 'Session Timing', 'Fees']
for col, header in enumerate(headers):
    worksheet.write(0, col, header)

names = ['Ajith', 'Surya', 'Narain', 'Kapil', 'Mokit', 'Shravan', 'Akil', 'Lakshimi']
months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = [2023, 2024]
attendance_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
session_types = ['Batting', 'Bowling', 'Fielding']

row = 1

for name in names:
    month_choice = random.choice(months)
    year_choice = random.choice(years)
    date_choice = random.choice(range(1, 29))
    date_of_join = f'{date_choice}/{month_choice}/{year_choice}'

    for practice_month in attendance_months:
        fees = 2500
        attendance_count = random.randint(15, 24)
        practice_hour = attendance_count * 2

        # Generate sorted unique practice dates
        practice_dates = random.sample(range(1, 29), attendance_count)
        practice_dates.sort()

        for date in practice_dates:
            session_choice = random.choice(session_types)
            if session_choice.lower() == 'batting':
                coach = 'Ravi Shankar'
                timing = '(6 to 8)am'
            elif session_choice.lower() == 'bowling':
                coach = 'Ravi Chandran'
                timing = '(4 to 6)pm'
            else:
                coach = 'Prabaharan'
                timing = '(8 to 9)am'

            # Fill all fields for every row
            worksheet.write(row, 0, name)
            worksheet.write(row, 1, date_of_join)
            worksheet.write(row, 2, attendance_count)
            worksheet.write(row, 3, practice_hour)
            worksheet.write(row, 4, practice_month)
            worksheet.write(row, 5, date)
            worksheet.write(row, 6, session_choice)
            worksheet.write(row, 7, coach)
            worksheet.write(row, 8, timing)
            worksheet.write(row, 9, fees)
            row += 1

workbook.close()
print("✅ Excel file created with realistic sorted practice dates!")
