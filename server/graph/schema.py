from graphene import Schema, ObjectType
from department import Department, Mutation as DepartmentMutation, Query as DepartmentQuery
from session import Session, Mutation as SessionMutation, Query as SessionQuery
from teacher import Teacher, Mutation as TeacherMutation, Query as TeacherQuery
from subject import Subject, Mutation as SubjectMutation, Query as SubjectQuery


class Query(DepartmentQuery,
            TeacherQuery,
            SessionQuery,
            SubjectQuery,
            ObjectType):
    pass


class Mutation(DepartmentMutation,
               TeacherMutation,
               SessionMutation,
               SubjectMutation,
               ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation,
                types=[Teacher, Department, Session, Subject])
