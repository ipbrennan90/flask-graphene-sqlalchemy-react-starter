from models.foundation import Base
from models.department import Department
from models.teacher import Teacher
from models.subject import Subject
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import (relationship, backref)


class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # registration_open = Column(DateTime, default=func.now())
    # registration_closed = Column(DateTime, default=func.now())
    # start_date = Column(DateTime, default=func.now())
    # end_date = Column(DateTime, default=func.now())
    room = Column(Integer)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('sessions',
                        uselist=True,
                        cascade='delete,all')
    )
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship(
        Subject,
        backref=backref('sessions',
                        uselist=True,
                        cascade='delete,all')
    )
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship(
        Teacher,
        backref=backref('sessions',
                        uselist=True,
                        cascade='delete,all')
    )
    total_students = Column(Integer)
