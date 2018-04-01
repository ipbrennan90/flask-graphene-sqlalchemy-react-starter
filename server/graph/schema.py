import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.department import Department as DepartmentModel
from models.teacher import Teacher as TeacherModel
import pdb


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
    all_departments = SQLAlchemyConnectionField(Department)
    teacher = graphene.Field(
        Teacher, name=graphene.String(), department=graphene.String())

    def resolve_teacher(self, info, **args):
        q = Teacher.get_query(info)
        daves = q.filter(
            (TeacherModel.name.contains(args.get('name'))) | (TeacherModel.department.name.contains(args.get('department')))).first()
        return daves


schema = graphene.Schema(query=Query, types=[Teacher, Department])
