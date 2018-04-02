from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import graphene
from graphene import relay
from models.department import Department as DepartmentModel
from models.foundation import db_session


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class CreateDepartment(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        new_department = DepartmentModel(name=name)
        db_session.add(new_department)
        db_session.commit()

        return CreateDepartment(id=new_department.id, name=new_department.name)


class Mutation(graphene.ObjectType):
    create_department = CreateDepartment.Field()


class Query(graphene.ObjectType):
    all_departments = SQLAlchemyConnectionField(Department)
    department = graphene.Field(Department, name=graphene.String())

    def resolve_department(self, info, **args):
        q = Department.get_query(info)
        department_result = q.filter(
            DepartmentModel.name.contains(args.get('name'))).first()
        return department_result
