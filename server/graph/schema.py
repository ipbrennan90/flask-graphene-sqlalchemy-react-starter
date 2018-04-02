import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models.department import Department as DepartmentModel
from models.teacher import Teacher as TeacherModel
from models.subject import Subject as SubjectModel
from models.session import Session as SessionModel
from models.foundation import db_session
import pdb


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Teacher(SQLAlchemyObjectType):
    class Meta:
        model = TeacherModel
        interfaces = (relay.Node, )


class Session(SQLAlchemyObjectType):
    class Meta:
        model = SessionModel
        interfaces = (relay.Node, )


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
    node = relay.Node.Field()
    all_teachers = SQLAlchemyConnectionField(Teacher)
    all_departments = SQLAlchemyConnectionField(Department)
    teacher = graphene.Field(Teacher, name=graphene.String())
    department = graphene.Field(Department, name=graphene.String())
    teachers = graphene.List(Teacher)

    def resolve_teacher(self, info, **args):
        q = Teacher.get_query(info)
        teacher_result = q.filter(
            TeacherModel.name.contains(args.get('name'))).first()
        return teacher_result

    def resolve_department(self, info, **args):
        q = Department.get_query(info)
        department_result = q.filter(
            DepartmentModel.name.contains(args.get('name'))).first()
        return department_result

    def resolve_teachers(self, info, **args):
        q = Teacher.get_query(info)
        return q.all()


class Mutation(graphene.ObjectType):
    create_department = CreateDepartment.Field()
    create_teacher = CreateTeacher.Field()
    create_subject = CreateSubject.Field()
    update_teacher = UpdateTeacher.Field()
    destroy_teacher = DestroyTeacher.Field()


schema = graphene.Schema(query=Query, mutation=Mutation,
                         types=[Teacher, Department, Subject])
