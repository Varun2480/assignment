
"""
REST API USING CRUD OPERATIONS
"""
import json
import datetime
import connexion   # for swagger
from flask import request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# *********************************************************************************************


app = connexion.App(__name__, specification_dir='./')    # where there is app use app.app
# pswd = quote('Varun@2480')
#
# engine = create_engine('mysql+pymysql://root:%s@localhost/mydatabase' % pswd)
engine = create_engine('mysql+pymysql://root:Varun2480@localhost/mydatabase')

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


Base = declarative_base()


class StudentInfo(Base):
    """this is a student class"""
    __tablename__ = "studentinfo"
    id = Column(Integer(), primary_key=True)
    name = Column(String(20), unique=False, nullable=False)
    class_id = Column(Integer(), ForeignKey("class.id"), unique=False, nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.now())
    updated_on = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    alembic_update = Column(String(20), unique=False, nullable=False)

    classInfo = relationship("ClassInfo")


class ClassInfo(Base):  # class name should match with db table name,
    """this is a class class"""
    __tablename__ = "class"
    id = Column(Integer(), primary_key=True)
    name = Column(String(20), unique=False, nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.now())
    updated_on = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


Base.metadata.create_all(bind=engine)


# *********************************************************************************************
# CRUD ---> create, read, update, delete

# insert/create


@app.route("/insert/student", methods=['POST'])
def insert_student():
    """this is insert method"""
    try:
        stuid = request.form.get('id')
        # inside get we need to mention the columns names in the table
        stuname = request.form.get('name')
        classid = request.form.get('class_id')

        entry = StudentInfo(id=stuid, name=stuname, class_id=classid)

        session.add(entry)
        session.commit()
        return_var = {"status": True, "msg": "data inserted successfully"}
    except Exception as ex:
        session.rollback()
        print("error while inserting data----->", ex)
        return_var = {"status": False, "msg": "class not found, check the input data correctly"}

    return jsonify(return_var)


# read


@app.route("/read/student", methods=['GET'])
def read_student():
    """this is read method"""
    try:
        temp = session.query(StudentInfo).all()
        temp_dic = {}
        count = 1
        for j in temp:
            # print(j, j.stu_id, j.stu_name, j.stu_age)
            # keys must be str, int, float, bool or None, not Student
            store = {"stuid": j.id, "stuname": j.name, "classid": j.class_id,
                     "created_on": str(j.created_on), "updated_on": str(j.updated_on)}
            temp_dic["row {}".format(count)] = store
            count += 1
        # print(temp_dic)
        return_var = {"status": True, "data": json.dumps(temp_dic)}
    except Exception as ex:
        print("error while reading data---->", ex)
        return_var = {"status": False, "msg": "unable to read the data"}
    return jsonify(return_var)

# update


@app.route("/update/student", methods=['PUT'])
def update_student():
    """this is update method"""
    try:
        stuid = request.form.get('id')
        entry = session.query(StudentInfo).get(stuid)
        entry.name = request.form.get('name')
        entry.class_id = request.form.get('class_id')

        session.commit()
        return_var = {"status": True, "msg": "data updated successfully"}
    except Exception as ex:
        session.rollback()
        print("error while updating data---->", ex)
        return_var = {"status": False, "msg": "class not found, check the input"}

    return jsonify(return_var)


# # delete
@app.route("/delete/student", methods=['DELETE'])
def delete_student():
    """this is delete method"""
    try:

        stuid = request.form.get('id')
        entry = session.query(StudentInfo).get(stuid)

        session.delete(entry)
        session.commit()

        return_var = {"status": True, "msg": "data deleted successfully"}
    except Exception as ex:
        session.rollback()
        print("error while deleting data---->", ex)
        return_var = {"status": False, "msg": "unable to delete the data"}
    return jsonify(return_var)


@app.route("/insert/class", methods=['POST'])
def insert_class():
    """this is insert method"""
    try:
        class_id = request.form.get('id')
        # inside get we need to mention the columns names in the table
        class_name = request.form.get('name')

        entry = ClassInfo(id=class_id, name=class_name)

        session.add(entry)
        session.commit()
        return_var = {"status": True, "msg": "data inserted successfully"}
    except Exception as ex:
        session.rollback()
        print("error while inserting data----->", ex)
        return_var = {"status": False, "msg": "cannot insert the data"}

    return jsonify(return_var)


@app.route("/read/class", methods=['GET'])
def read_class():
    """this is read method"""
    try:
        temp = session.query(ClassInfo).all()
        temp_dic = {}
        count = 1
        for j in temp:
            store = {"class_id": j.id, "class_name": j.name,
                     "created_on": str(j.created_on), "updated_on": str(j.updated_on)}
            temp_dic["row {}".format(count)] = store
            count += 1
        # print(temp_dic)
        return_var = {"status": True, "data": json.dumps(temp_dic)}
    except Exception as ex:
        print("error while reading data---->", ex)
        return_var = {"status": False, "msg": "unable to read the data"}
    return jsonify(return_var)


@app.route("/update/class", methods=['PUT'])
def update_class():
    """this is update method"""
    try:
        class_id = request.form.get('id')
        entry = session.query(ClassInfo).get(class_id)
        entry.name = request.form.get('name')

        session.commit()

        return_var = {"status": True, "msg": "data updated successfully"}
    except Exception as ex:
        session.rollback()
        print("error while updating data---->", ex)
        return_var = {"status": False, "msg": "cannot update the data"}

    return jsonify(return_var)


@app.route("/delete/class", methods=['DELETE'])
def delete_class():
    """this is delete method"""
    try:
        class_id = request.form.get('id')
        entry = session.query(ClassInfo).get(class_id)

        session.delete(entry)
        session.commit()

        return_var = {"status": True, "msg": "data deleted successfully"}
    except Exception as ex:
        session.rollback()
        print("error while deleting data---->", ex)
        return_var = {"status": False, "msg": "unable to delete the data"}
    return jsonify(return_var)


# running this in the assignment_server.py
