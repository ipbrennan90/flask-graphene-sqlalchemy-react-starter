from models.foundation import engine, db_session, Base
from models.department import Department
from models.teacher import Teacher
Base.metadata.create_all(bind=engine)

engineering = Department(name='Engineering')
computer_science = Department(name='Computer Science')
dat_boi = Department(name="Dat Boi")
db_session.add(engineering)
db_session.add(computer_science)
db_session.add(dat_boi)

patrick = Teacher(name='Poot', department=dat_boi)
justin = Teacher(name='Justin', department=engineering)
david = Teacher(name='David', department=computer_science)
db_session.add(patrick)
db_session.add(justin)
db_session.add(david)

db_session.commit()
