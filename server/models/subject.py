from models.foundation import Base
from models.department import Department
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import (relationship, backref)


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('subjects',
                        uselist=True,
                        cascade='delete,all')
    )
