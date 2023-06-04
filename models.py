from app import db
from sqlalchemy import UniqueConstraint


class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(100), nullable = False)

    __table_args__ = (
        db.UniqueConstraint(name,name='ux_usr_name'),
        db.UniqueConstraint(email,name='ux_eml_name'),
    )

    def __init__(self, name='', password='', email=''):
        self.name = name
        self.password = password
        self.email = email

  
class Permissions(db.Model):
    __tablename__ = 'permission'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)

    __table_args__ = (
        db.UniqueConstraint(name,name='ux_prm_name'),
    )


class Roles(db.Model):
    __tablename__ = 'role'
  
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)

    __table_args__ = (
        db.UniqueConstraint(name,name='ux_role_name'),
    )


class Matrix(db.Model):
    __tablename__ = 'matrix'
    
    id = db.Column('id', db.Integer, primary_key = True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)

    __table_args__ = (
        db.UniqueConstraint(permission_id,role_id,name='ux_perm_role_matrix'),
    )


class UserMatrix(db.Model):
    __tablename__ = 'umatrix'
   
    id = db.Column('id', db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)

    __table_args__ = (
        db.UniqueConstraint(user_id, role_id, name='ux_usr_role_matrix'),
    )
