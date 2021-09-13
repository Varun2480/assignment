
"""
REST API USING CRUD OPERATIONS
"""

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
    # alembic_update = Column(String(20), unique=False, nullable=False)

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


@app.route("/student/add_data", methods=['POST'])
def insert_student():
    """this is insert method"""
    try:
        student_id = request.form.get('id')
        # inside get we need to mention the columns names in the table
        student_name = request.form.get('name')
        class_id = request.form.get('class_id')

        entry = StudentInfo(id=student_id, name=student_name, class_id=class_id)

        session.add(entry)
        session.commit()
        return_var = {"status": True, "msg": "data inserted successfully"}
    except Exception as ex:
        session.rollback()
        print("error while inserting data----->", ex)
        return_var = {"status": False, "msg": "class not found, check the input data correctly"}

    return jsonify(return_var)


# read


@app.route("/student/info", methods=['GET'])
def read_student():
    """this is read method"""
    try:
        rows = session.query(StudentInfo).all()
        data = []
        for row in rows:

            data.append(["student_id = {}".format(row.id),
                        "student_name = {}".format(row.name),
                         "class_id = {}".format(row.class_id),
                         "created_on = {}".format(str(row.created_on)),
                         "updated_on = {}".format(str(row.updated_on))])
        # print(temp_dic)
        # return_var = {"status": True, "data": json.dumps(temp_dic)}
        return_var = {"status": True, "data": data}
    except Exception as ex:
        print("error while reading data---->", ex)
        return_var = {"status": False, "msg": "unable to read the data"}
    return jsonify(return_var)

# update


@app.route("/student/edit", methods=['PUT'])
def update_student():
    """this is update method"""
    try:

        updated_data = [dict(id=request.form.get('id'), name=request.form.get('name'),
                             class_id=request.form.get('class_id'))]

        session.bulk_update_mappings(StudentInfo, updated_data)

        session.commit()
        return_var = {"status": True, "msg": "data updated successfully"}
    except Exception as ex:
        session.rollback()
        print("error while updating data---->", ex)
        return_var = {"status": False, "msg": "class not found, check the input"}

    return jsonify(return_var)


# # delete
@app.route("/student/remove", methods=['DELETE'])
def delete_student():
    """this is delete method"""
    try:

        student_id = request.form.get('id')
        entry = session.query(StudentInfo).get(student_id)

        session.delete(entry)
        session.commit()

        return_var = {"status": True, "msg": "data deleted successfully"}
    except Exception as ex:
        session.rollback()
        print("error while deleting data---->", ex)
        return_var = {"status": False, "msg": "unable to delete the data"}
    return jsonify(return_var)


@app.route("/class/add_data", methods=['POST'])
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


@app.route("/class/info", methods=['GET'])
def read_class():
    """this is read method"""
    try:
        rows = session.query(ClassInfo).all()
        data = []
        for row in rows:

            data.append(["class_id = {}".format(row.id),
                         "class_name = {}".format(row.name),
                         "created_on = {}".format(row.created_on),
                         "updated_on = {}".format(row.updated_on)])
        # print(temp_dic)
        return_var = {"status": True, "data": data}
    except Exception as ex:
        print("error while reading data---->", ex)
        return_var = {"status": False, "msg": "unable to read the data"}
    return jsonify(return_var)


@app.route("/class/edit", methods=['PUT'])
def update_class():
    """this is update method"""
    try:
        # class_id = request.form.get('id')
        # entry = session.query(ClassInfo).get(class_id)
        # entry.name = request.form.get('name')

        updated_data = [dict(id=request.form.get('id'), name=request.form.get('name'))]

        session.bulk_update_mappings(ClassInfo, updated_data)

        session.commit()

        return_var = {"status": True, "msg": "data updated successfully"}
    except Exception as ex:
        session.rollback()
        print("error while updating data---->", ex)
        return_var = {"status": False, "msg": "cannot update the data"}

    return jsonify(return_var)


@app.route("/class/remove", methods=['DELETE'])
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
