import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.session import Session as SessionModel
from models.foundation import db_session
from department import Department
from teacher import Teacher
from subject import Subject


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
        dept = Department.get_query(info).filter_by(id=department).one()
        teacher = Teacher.get_query(info).filter_by(id=teacher).one()
        subject = Subject.get_query(info).filter_by(id=subject).one()
        new_session = SessionModel(
            name=name, department=dept, subject=subject, teacher=teacher, room=room)
        db_session.add(new_session)
        db_session.commit()

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
