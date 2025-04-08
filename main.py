from collections import defaultdict

from database import session, Student, Coach
from datetime import datetime


def session_attended_3_months(name):
    target_months = ['Jan', 'Feb', 'Mar']

    students = (
        session.query(Student).filter(Student.name == name).all())

    print(f"📌 {name} attended in these months:")
    result = 0
    for student in students:
        for attendance in student.attendances:
            if attendance.month in target_months:
                result += attendance.total_session
    print(f"You have attended {result} in past 3 Months ")


#session_attended_3_months('Narain')


def student_fees(name):
    students = session.query(Student).filter_by(name=name).all()
    for student in students:
        for fees in student.coaching_fees:
            print(f'Your Coaching Fees is {fees.fees}')


#student_fees('Surya')


def any_month_session(name, month):
    target_month = month
    students = session.query(Student).filter_by(name=name).all()
    for student in students:
        for attendance in student.attendances:
            if attendance.month == target_month:
                print(
                    f'📅 You have {attendance.total_session} sessions in {month}\nHere is the list of {attendance.total_session} sessions')
        count = 1
        for sess in student.sessions:
            if sess.month == target_month:
                print(
                    f"{count}. On {sess.month} {sess.practice_date}, you have a {sess.session} session at {sess.coaching_time} with Coach {sess.coach_name}")
                count += 1


#any_month_session('Ajith', 'Mar')


def current_month_remaining_session(name, month):
    target_month = month
    today = datetime.today()

    students = session.query(Student).filter_by(name=name).all()
    count = 1
    seen = set()

    for student in students:
        for sesssion in student.sessions:
            if sesssion.month == target_month and sesssion.practice_date > today.day:
                key = (sesssion.month, sesssion.practice_date, sesssion.session, sesssion.coaching_time,
                       sesssion.coach_name)
                if key not in seen:
                    print(
                        f"{count}. You still have a {sesssion.session} session on {sesssion.month} {sesssion.practice_date} at {sesssion.coaching_time} with Coach {sesssion.coach_name}")
                    seen.add(key)
                    count += 1


#current_month_remaining_session('Kapil', 'Apr')


#coach
def current_month_rem_session(coach_name, month):
    today_day = datetime.today().day

    coach = session.query(Coach).filter_by(name=coach_name).first()
    if not coach:
        print(f"❌ Coach '{coach_name}' not found.")
        return

    # Filter relevant sessions
    remaining_sessions = [
        sess for sess in coach.sessions
        if sess.month.lower() == month.lower() and sess.practice_date >= today_day
    ]

    if not remaining_sessions:
        print(f"✅ No remaining sessions for Coach {coach_name} in {month}.")
        return

    # Group sessions by (practice_date, coaching_time)
    grouped_sessions = defaultdict(list)
    for sess in remaining_sessions:
        key = (sess.practice_date, sess.coaching_time)
        grouped_sessions[key].append(sess.student.name)

    print(f"📅 Remaining sessions for Coach {coach_name} in {month}:")
    for i, ((date, time), student_names) in enumerate(sorted(grouped_sessions.items()), start=1):
        students_str = ", ".join(sorted(student_names))
        print(f"{i}. {month} {date} at {time} for Student ({students_str})")


#current_month_rem_session('Ravi Chandran', 'Apr')


def coach_team(coach_name):
    coach = session.query(Coach).filter_by(name=coach_name).first()
    if not coach:
        print(f"❌ Coach '{coach_name}' not found.")
        return

    if not coach.students:
        print(f"ℹ️ Coach {coach_name} has no students.")
        return

    print(f"👥 Team under Coach {coach_name}:")
    for i, student in enumerate(coach.students, start=1):
        print(f"{i}. {student.name}")


#coach_team('Ravi Shankar')


def class_attended_for_coach(coach_name, month):
    coach = session.query(Coach).filter_by(name=coach_name).first()
    if not coach:
        print(f"❌ Coach '{coach_name}' not found.")
        return

    attendance_count = {}

    for session_ in coach.sessions:
        if session_.month.lower() == month.lower():
            student_name = session_.student.name
            attendance_count[student_name] = attendance_count.get(student_name, 0) + 1

    print(f"📊 Session counts for Coach {coach_name} in {month}:")
    for student_name, count in attendance_count.items():
        print(f"👤 {student_name}: {count} sessions")

#class_attended_for_coach('Prabaharan','Feb')


#Admin

def attendace_per_person(name,month):
    students = session.query(Student).filter_by(name=name).all()
    for student in students:
        for attendace in student.attendances:
            if attendace.month.lower() == month.lower():
                print(f'{student.name} have attended {attendace.total_session} in {month}')


#attendace_per_person('Akil','Jan')


def total_sessions_for_coach_in_month(coach_name, month):
    coach = session.query(Coach).filter_by(name=coach_name).first()
    if not coach:
        print(f"❌ Coach '{coach_name}' not found.")
        return

    unique_dates = set()

    for session_ in coach.sessions:
        if session_.month.lower() == month.lower():
            unique_dates.add(session_.practice_date)

    count = len(unique_dates)

    print(f"📊 Coach {coach_name} has conducted {count} sessions in {month}.")


#total_sessions_for_coach_in_month('Ravi Chandran','jan')


def fees_collection(month):
    total_fees = 0
    students = session.query(Student).all()

    for student in students:
        has_session_in_month = any(
            sesssion.month and sesssion.month.lower() == month.lower()
            for sesssion in student.sessions
        )
        if has_session_in_month:
            for fees in student.coaching_fees:
                total_fees += fees.fees

    print(f"💰 Total coaching fees collected in {month}: ₹{total_fees}")


#fees_collection('Jan')


def per_student_session_details_for_particular_month(name, month):
    student = session.query(Student).filter_by(name=name).first()
    if not student:
        print(f"❌ Student '{name}' not found.")
        return

    print(f"📘 Sessions for {name}:")
    count = 1
    for session_ in student.sessions:
        if session_.month.lower() == month.lower():
            print(f"{month} {count}. {session_.practice_date} - {session_.session} at {session_.coaching_time} with Coach {session_.coach_name}")
            count += 1


#per_student_session_details_for_particular_month('Mokit', 'Feb')


def overall_session_detail():
    students = session.query(Student).all()
    count = 1
    today = datetime
    for student in students:
        for sesssion in student.sessions:
            print(
                f"{count}. {sesssion.month} {sesssion.practice_date} - {student.name} | {sesssion.session} | {sesssion.coaching_time} | Coach: {sesssion.coach_name}")
            count += 1


overall_session_detail()
