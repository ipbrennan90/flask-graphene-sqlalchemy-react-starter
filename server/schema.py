import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.department import Department as DepartmentModel
from models.teacher import Teacher as TeacherModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Teacher(SQLAlchemyObjectType):
    class Meta:
        model = TeacherModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_teachers = SQLAlchemyConnectionField(Teacher)


schema = graphene.Schema(query=Query)
