from flask import  Flask, Blueprint, render_template, request, redirect, url_for
from sqlalchemy import inspect

main = Blueprint("main", __name__)


@main.route('/signup')
def view_signup():
   """Render signup view"""
   se = request.args['se'] if 'se' in request.args else None
   return render_template('signup.html', se=se)


@main.route("/api/signup", methods = ['POST'])
def signup():
   """POST => Create user 
   """

   from app import db
   from models import Users

   name, password, email = request.form['name'], request.form['password'], request.form['email']
   try: 
      if name.strip() and password.strip() and email.strip():
         user = Users(
            name=name,
            password=password,
            email=email
         )
         db.session.add(user)
         db.session.commit()
         print('INFO: User Created')
      else:
         print('ERR: Invalid Signup')
         return redirect(url_for('main.view_signup', se=True))

      return redirect(url_for('index'))
   except:
      # EXISTING USER
      print('ERR: SIGNUP')
      return redirect(url_for('main.view_signup', se=True))
      

@main.route("/api/login", methods = ['POST'])
def login():
   """POST => If user exist, go to dashboard
            If user doesn't exist, show message
   """

   from models import Users

   query = Users.query

   print(query.all())
   name, password = request.form['name'], request.form['pass']
   user = query.filter((Users.name==name) | (Users.email==name)).first()

   if user and user.password == password:
      print('INFO: User exists')
      return redirect(url_for('main.user_permission', id=user.id))
   else:
      print('INFO: User doesnt exists')
      return redirect(url_for('index', ne=True))


def object_as_dict(obj):
   """Return object as dict"""
   if isinstance(obj, list):
      params = []
      for ob in obj:
         params.append({
            c.key: getattr(ob, c.key)
            for c in inspect(ob).mapper.column_attrs
         })
      return params
   return {c.key: getattr(obj, c.key)
         for c in inspect(obj).mapper.column_attrs}


# API CALLS => RUN TO POSTMAN TO FETCH AND INSERT DATA
@main.route("/api/roles", methods = ['GET', 'POST'])
def roles(int=None):
   """GET => will return all available roles
      POST:lst param str [{'name': 'staff' }] => will create defined roles in a list
   """

   from app import db
   from models import Roles
   
   if request.method == 'GET':
      roles = Roles.query.all()
      return object_as_dict(roles)

   elif request.method == 'POST':
      try:
         roles = request.get_json()

         for role in roles:
            role = Roles(
               name=role['name'].strip(),
            )
            db.session.add(role)

         db.session.commit()
         return roles
      except:
         return {
            'ERROR': 'Invalid Role'
         }
  

@main.route("/api/roles/<int:id>/permissions", methods = ['GET', 'POST'])
def role_matrix(id):
   """GET => will return list of permissions based on the passed id
      POST: param int { 'permissions': [<id of permission>] }
   """

   from app import db
   from models import Roles, Permissions, Matrix
   
   if request.method == 'GET':
      role_id = Roles.query.filter_by(id=id).first()

      if role_id:
         data = db.session.query(Roles, Permissions, Matrix) \
                  .filter( Roles.id == Matrix.role_id,
                           Permissions.id == Matrix.permission_id,
                           Roles.id == role_id.id ).all()
         permissions = []
         for d in data:
            permission = object_as_dict(d[1])
            permissions.append(permission)

         return permissions
      else:  
         return {
            'ERROR': 'Invalid Role'
         }

   elif request.method == 'POST':
      matrix = request.get_json()
      role_id = Roles.query.filter_by(id=id).first()
      errors = []
   
      try:
         if role_id and 'permissions' in matrix and matrix['permissions']:
            permissions = []
            for prm in matrix['permissions']:
               permission_id = Permissions.query.filter_by(id=prm).first()
               if permission_id:
                  permissions.append(permission_id)
               else:
                  errors.append({'PERMISSION': 'Invalid Permission'})
                  break

            if permissions and role_id:
               for permission_id in permissions:
                  _matrix = Matrix(
                     permission_id=permission_id.id,
                     role_id=role_id.id
                  )

               db.session.add(_matrix)
            db.session.commit()
         else:
            if role_id is None:
               errors.append({'ROLE': 'Invalid Role'})
            if 'permissions' not in matrix:
               errors.append({'REQUEST': 'Invalid'})
            return {
               'ERROR': errors
            }
         return matrix
      except:
         return {
            'ERROR': 'Invalid Matrix'
         }
      

@main.route("/api/permissions", methods = ['GET', 'POST'])
def permissions():
   """GET => will return all available permissions in a list
      POST:lst param str [{'name': 'create' }] => will create defined permisiions in a list
   """

   from app import db
   from models import Permissions
   
   if request.method == 'GET':
      permissions = Permissions.query.all()
      return object_as_dict(permissions)

   elif request.method == 'POST':
      permissions = request.get_json()
      try:
         for permission in permissions:
            permission = Permissions(
               name=permission['name'].strip(),
            )

            db.session.add(permission)
         db.session.commit()
         return permissions
      except:
         return {
            'ERROR': 'Invalid Permission'
         }


@main.route("/api/users/<int:id>/roles", methods = ['GET', 'POST'])
def user_role(id):
   """GET => will return list of roles of user
      POST: param [{ 'roles': [<id of permission>] }] 
   """

   from app import db
   from models import Roles, Users, UserMatrix, Matrix
   
   if request.method == 'GET':
      user_id = Users.query.filter_by(id=id).first()

      if user_id:
         data = db.session.query(Roles, Users, UserMatrix) \
                  .filter( Roles.id == UserMatrix.role_id,
                           Users.id == UserMatrix.user_id,
                           Users.id == user_id.id ).all()
         roles = []
         for d in data:
            role = object_as_dict(d[0])
            roles.append(role)

         return roles
      else:  
         return {
            'ERROR': 'Invalid User'
         }

   elif request.method == 'POST':
      try:
         matrix = request.get_json()
         user_id = Users.query.filter_by(id=id).first()
         errors = []
       
         if user_id and 'roles' in matrix and matrix['roles']:
            roles = []
            for role in matrix['roles']:
               role_id = Roles.query.filter_by(id=role).first()
               roles.append(role_id.id)
            
            if user_id and roles:
               for role_id in roles:
                  _matrix = UserMatrix(
                     role_id=role_id,
                     user_id=user_id.id
                  )

                  db.session.add(_matrix)
               db.session.commit()
         else:
            if user_id is None:
               errors.append({'USER': 'Invalid User'})
            if 'roles' not in matrix:
               errors.append({'REQUEST': 'Invalid'})
            return {
               'ERROR': errors
            }
         return matrix
      except:
         return {
            'ERROR': 'Invalid User Matrix'
         }


@main.route("/api/users/<int:id>/permissions", methods = ['GET'])
def user_permission(id):
   """GET => will return list of permissions based on the passed id
   """

   from app import db
   from models import Roles, Users, UserMatrix, Matrix, Permissions
   
   user_id = Users.query.filter_by(id=id).first()
   
   if user_id is None:
      return { 'ERROR': 'Invalid User'}

   data = db.session.query(Users, UserMatrix, Roles, Matrix, Permissions) \
            .filter( Users.id == UserMatrix.user_id,
                     Users.id == user_id.id,
                     Roles.id == UserMatrix.role_id,
                     Roles.id == Matrix.role_id,
                     Permissions.id == Matrix.permission_id ).all()

   permissions = []
   for d in data:
      permission = object_as_dict(d[4])
      permissions.append(permission)

   return render_template('user.html', user=user_id.name, permisssions=permissions)
