import pandas as pd
from sqlalchemy import create_engine, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship, Mapped, mapped_column
from typing import List

# --- Database setup ---
db_url = "mysql+mysqlconnector://root:AjithRavi!25@localhost/cricketcoaching"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


# --- SQLAlchemy Models ---
class Base(DeclarativeBase):
    pass


class StudentCoach(Base):
    __tablename__ = 'student_coach'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'))
    coach_id: Mapped[int] = mapped_column(Integer, ForeignKey('coaches.id'))


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    date_of_joining: Mapped[str] = mapped_column(String(255))

    coaches: Mapped[List['Coach']] = relationship('Coach', secondary='student_coach', back_populates='students')
    sessions: Mapped[List['SessionType']] = relationship('SessionType', back_populates='student')
    attendances: Mapped[List['Attendance']] = relationship('Attendance', back_populates='student')
    coaching_fees: Mapped[List['CoachingFees']] = relationship('CoachingFees', back_populates='student')


class Coach(Base):
    __tablename__ = 'coaches'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    coaching_time: Mapped[str] = mapped_column(String(255), nullable=True)
    session: Mapped[str] = mapped_column(String(255), nullable=True)

    students: Mapped[List['Student']] = relationship(
        'Student', secondary='student_coach', back_populates='coaches')
    sessions: Mapped[List['SessionType']] = relationship('SessionType', back_populates='coach')


class SessionType(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    practice_date: Mapped[int]
    month: Mapped[str] = mapped_column(String(255), nullable=True)
    coaching_time: Mapped[str] = mapped_column(String(255), nullable=True)
    session: Mapped[str] = mapped_column(String(255), nullable=True)
    coach_name: Mapped[str] = mapped_column(String(255), nullable=True)

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'))
    student: Mapped['Student'] = relationship('Student', back_populates='sessions')
    coach: Mapped['Coach'] = relationship('Coach', back_populates='sessions')
    coach_id: Mapped[int] = mapped_column(Integer, ForeignKey('coaches.id'))


class Attendance(Base):
    __tablename__ = 'attendances'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_session: Mapped[int]
    month: Mapped[str] = mapped_column(String(50))

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'))
    student: Mapped['Student'] = relationship('Student', back_populates='attendances')


class CoachingFees(Base):
    __tablename__ = 'coaching_fees'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fees: Mapped[int]

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'))
    student: Mapped['Student'] = relationship('Student', back_populates='coaching_fees')


Base.metadata.create_all(engine)

df = pd.read_excel('Cricket Coaching.xlsx', sheet_name='firstsheet')

required_fields = ['Name', 'Date of Join', 'Coach', 'Session Type', 'Session Timing', 'Attendance', 'Month']

for index, row in df.iterrows():
    if any(pd.isna(row[field]) for field in required_fields):
        continue

    coach = session.query(Coach).filter_by(name=row['Coach']).first()
    if not coach:
        coach = Coach(
            name=row['Coach'],
            coaching_time=row['Session Timing'],
            session=row['Session Type']
        )
        session.add(coach)
        session.commit()

    # --- Check or Create Student ---
    student = session.query(Student).filter_by(name=row['Name']).first()
    if not student:
        student = Student(
            name=row['Name'],
            date_of_joining=row['Date of Join'],

        )
        session.add(student)
        session.commit()

    existing_session = session.query(SessionType).filter_by(
        practice_date=row['Practice date'],
        month=row['Month'],
        student_id=student.id,
        coach_id=coach.id,
        session=row['Session Type'],
        coaching_time=row['Session Timing']
    ).first()

    if not existing_session:
        session_type = SessionType(
            practice_date=row['Practice date'],
            month=row['Month'],
            coaching_time=row['Session Timing'],
            session=row['Session Type'],
            coach_name=row['Coach'],
            student_id=student.id,
            coach_id=coach.id
        )
        session.add(session_type)

    # --- Link Student and Coach ---
    link_exists = session.query(StudentCoach).filter_by(student_id=student.id, coach_id=coach.id).first()
    if not link_exists:
        link = StudentCoach(student_id=student.id, coach_id=coach.id)
        session.add(link)
        session.commit()

    # --- Add Attendance (once per student per month) ---
    existing_attendance = session.query(Attendance).filter_by(
        student_id=student.id,
        month=row['Month']
    ).first()

    if not existing_attendance:
        attendance = Attendance(
            total_session=int(row['Attendance']),
            month=row['Month'],
            student_id=student.id
        )
        session.add(attendance)

    # --- Add Coaching Fee (only once per student) ---
    existing_fee = session.query(CoachingFees).filter_by(student_id=student.id).first()
    if not existing_fee:
        fee = CoachingFees(
            fees=2500,
            student_id=student.id
        )
        session.add(fee)
