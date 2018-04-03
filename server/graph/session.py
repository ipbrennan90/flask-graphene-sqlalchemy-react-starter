import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.teacher import Teacher as TeacherModel
from models.subject import Subject as SubjectModel
from models.session import Session as SessionModel
from models.department import Department as DepartmentModel
from models.foundation import db_session
from department import Department
from subject import Subject
from teacher import Teacher

from sqlalchemy import exists


class Session(SQLAlchemyObjectType):
    class Meta:
        model = SessionModel
        interfaces = (relay.Node, )


class CreateSession(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    department = graphene.Field(Department)
    subject = graphene.Field(Subject)
    teacher = graphene.Field(Teacher)
    room = graphene.String()

    class Arguments:
        department = graphene.Int()
        teacher = graphene.Int()
        subject = graphene.Int()
        name = graphene.String()
        room = graphene.Int()

    def mutate(self, info, name, department, subject, teacher, room):
        dept_exists = db_session.query(exists().where(
            DepartmentModel.id == department)).scalar()
        teacher_exists = db_session.query(
            exists().where(TeacherModel.id == teacher)).scalar()
        subject_exists = db_session.query(
            exists().where(SubjectModel.id == subject)).scalar()
        if dept_exists and teacher_exists and subject_exists:
            new_session = SessionModel(
                name=name, department_id=department, subject_id=subject, teacher_id=teacher, room=room)
            db_session.add(new_session)
            db_session.commit()
        else:
            exception_string = 'Error! '
            if not dept_exists:
                exception_string = exception_string + \
                    'department with id {} was not found '.format(department)
            if not teacher_exists:
                exception_string = exception_string + \
                    'teacher with id {} was not found '.format(teacher)
            if not subject_exists:
                exception_string = exception_string + \
                    'subject with id {} was not found '.format(subject)

            raise Exception(exception_string)

        return CreateSession(
            id=new_session.id,
            name=new_session.name,
            department=new_session.department,
            subject=new_session.subject,
            teacher=new_session.teacher,
            room=new_session.room
        )


class Query(graphene.ObjectType):
    all_sessions = SQLAlchemyConnectionField(Session)
    sessions = graphene.List(Session)

    def resolve_sessions(self, info, **args):
        q = Session.get_query(info)
        return q.all()


class Mutation(graphene.ObjectType):
    create_session = CreateSession.Field()
