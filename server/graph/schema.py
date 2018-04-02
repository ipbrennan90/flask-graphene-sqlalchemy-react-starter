import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.department import Department as DepartmentModel
from models.subject import Subject as SubjectModel
from models.session import Session as SessionModel
from department import Department, Mutation as DepartmentMutation, Query as DepartmentQuery
from teacher import Teacher, Mutation as TeacherMutation, Query as TeacherQuery


class Session(SQLAlchemyObjectType):
    class Meta:
        model = SessionModel
        interfaces = (relay.Node, )


class Subject(SQLAlchemyObjectType):
    class Meta:
        model = SubjectModel
        interfaces = (relay.Node, )


class Session(SQLAlchemyObjectType):
    class Meta:
        model = SessionModel
        interfaces = (relay.Node, )


class CreateSubject(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    department = graphene.Field(Department)

    class Arguments:
        department = graphene.Int()
        name = graphene.String()

    def mutate(self, info, name, department):
        q = Department.get_query(info)
        subject_department = q.filter_by(id=department).one()
        new_subject = SubjectModel(name=name, department=subject_department)
        db_session.add(new_subject)
        db_session.commit()

        return CreateSubject(id=new_subject.id, name=new_subject.name, department=new_subject.department)


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


class Query(DepartmentQuery,
            TeacherQuery,
            graphene.ObjectType):
    pass


class Mutation(DepartmentMutation,
               TeacherMutation,
               graphene.ObjectType):
    create_subject = CreateSubject.Field()
    create_session = CreateSession.Field()


schema = graphene.Schema(query=Query, mutation=Mutation,
                         types=[Teacher, Department, Subject])
