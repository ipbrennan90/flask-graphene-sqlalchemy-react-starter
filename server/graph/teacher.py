import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.teacher import Teacher as TeacherModel
from models.foundation import db_session
from department import Department


class Teacher(SQLAlchemyObjectType):
    class Meta:
        model = TeacherModel
        interfaces = (relay.Node, )


class CreateTeacher(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    department = graphene.Field(Department)

    class Arguments:
        department = graphene.Int()
        name = graphene.String()

    def mutate(self, info, name, department):
        q = Department.get_query(info)
        teacher_department = q.filter_by(id=department).first()
        new_teacher = TeacherModel(name=name, department=teacher_department)
        db_session.add(new_teacher)
        db_session.commit()

        return CreateTeacher(id=new_teacher.id, name=new_teacher.name, department=teacher_department)


class UpdateTeacher(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    department = graphene.Field(Department)

    class Arguments:
        id = graphene.Int()
        department = graphene.Int()
        name = graphene.String()

    def mutate(self, info, id, name=None, department=None):
        q = Teacher.get_query(info)
        teacher = q.filter_by(id=id).one()
        update_data = {}
        if name:
            update_data.update({'name': name})
        if department:
            update_data.update({'department_id': department})
        for key, value in update_data.iteritems():
            setattr(teacher, key, value)
            db_session.commit()

        return UpdateTeacher(id=teacher.id, name=teacher.name, department=teacher.department)


class DestroyTeacher(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        q = Teacher.get_query(info)
        teacher = q.filter_by(id=id).one()
        db_session.delete(teacher)
        db_session.commit()

        return DestroyTeacher(id=teacher.id, name=teacher.name)


class Query(graphene.ObjectType):
    all_teachers = SQLAlchemyConnectionField(Teacher)
    teacher = graphene.Field(Teacher, name=graphene.String())
    teachers = graphene.List(Teacher)

    def resolve_teacher(self, info, **args):
        q = Teacher.get_query(info)
        teacher_result = q.filter(
            TeacherModel.name.contains(args.get('name'))).first()
        return teacher_result

    def resolve_teachers(self, info, **args):
        q = Teacher.get_query(info)
        return q.all()


class Mutation(graphene.ObjectType):
    create_teacher = CreateTeacher.Field()
    update_teacher = UpdateTeacher.Field()
    destroy_teacher = DestroyTeacher.Field()
