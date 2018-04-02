import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.subject import Subject as SubjectModel
from models.foundation import db_session
from department import Department


class Subject(SQLAlchemyObjectType):
    class Meta:
        model = SubjectModel
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


class Query(graphene.ObjectType):
    all_subjects = SQLAlchemyConnectionField(Subject)
    subjects = graphene.List(Subject)

    def resolve_subjects(self, info, **args):
        q = Subject.get_query(info)
        return q.all()


class Mutation(graphene.ObjectType):
    create_subject = CreateSubject.Field()
