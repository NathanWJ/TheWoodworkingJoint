from flask_app import app
from flask import flash, render_template, redirect, request, session
#Models
from flask_app.models.woodproject import Woodproject
from flask_app.models.user import User
#Image upload: 
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.path.abspath('../Woodworking_Joint/flask_app/static/user_img/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


###################################### 
# CREATE 
###################################### 

@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("create.html",user=User.get_one_by_id(data))



@app.route('/create/woodproject', methods=['POST']) 
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    #Validation of non-image fields: 
    if not Woodproject.validate_woodproject(request.form):
        return redirect('/new')
    #Validation of image fields: 
    if 'woodProjectImg' not in request.files:
        flash('No file selected. Upload an image.')
        print("IMAGE VALIDATION - No File Selected")
        return redirect('/new')
    #Creates the file variable connected to the HTML 
    file = request.files['woodProjectImg']
    if file.filename == '':
        flash("Rename image and then reupload.")
        print("IMAGE VALIDATION - Filed Not Named")
        return redirect('/new')
    #If image file exists, then save it
    if file:
        print("IMAGE VALIDATION - Start saving file")
        filename = secure_filename(file.filename)
        # image_path = str(UPLOAD_FOLDER)+file.filename
        image_path = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("IMAGE VALIDATION - File saved here:", image_path)
    #Saves the form and the image's path to the db
    data = {
        "project_name": request.form["project_name"],
        "skill_level": request.form["skill_level"],
        "type": request.form["type"],
        "description": request.form["description"],
        "image_path" : image_path,
        "user_id": session["user_id"]
    }
    Woodproject.save(data)
    return redirect('/dashboard')



###################################### 
# HOME ROUTE
###################################### 

@app.route('/')
def index():
    return render_template('index.html')


###################################### 
# DASHBOARD
###################################### 

#View all
@app.route('/dashboard')
def results():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_one_by_id(data), woodprojects=Woodproject.get_all())

#View my projects
@app.route('/dashboard/myprojects')
def mywoodprojects():
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = {
        "user_id":session['user_id'],#This is the user_id as the foreign key within woodprojects to woodprjects by user
        "id":session['user_id'] #This id is for the user query to display the user's info
    }
    return render_template("dashboard.html", woodprojects=Woodproject.get_all_woodprojects_by_one_user(user_id), user=User.get_one_by_id(user_id))


#View filtered projects based on search
@app.route('/dashboard/mysearch')
def mysearch():
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = {
        "user_id":session['user_id'],#This is the user_id as the foreign key within woodprojects to woodprjects by user
        "id":session['user_id'] #This id is for the user query to display the user's info
    }
    data = {
        "skill_level": request.form["skill_level"],
        "type": request.form["type"],
    }
    return render_template("dashboard.html", woodprojects=Woodproject.get_all_woodprojects_by_user_search(data), user=User.get_one_by_id(user_id))




###################################### 
# ROUTE TO READ 
###################################### 

@app.route('/woodproject/<int:id>')
def woodproject(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view.html", woodproject=Woodproject.get_one_woodproject_by_id(data), user=User.get_one_by_id(user_data))


###################################### 
# UPDATE 
###################################### 

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id #This is the woodproject's ID
    } 
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html", woodproject=Woodproject.get_one_woodproject_by_id(data), user=User.get_one_by_id(user_data))

@app.route('/update/woodproject',methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Woodproject.validate_woodproject(request.form):
        return redirect('/new')
    data = {
        "project_name": request.form["project_name"],
        "skill_level": request.form["skill_level"],
        "type": request.form["type"],
        "description": request.form["description"],
        "id": request.form["id"]
    }
    Woodproject.update(data)
    return redirect("/dashboard")

@app.route('/edit/<int:id>/image')
def edit_with_image(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id #This is the woodproject's ID
    } 
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_image.html", woodproject=Woodproject.get_one_woodproject_by_id(data), user=User.get_one_by_id(user_data))


@app.route('/update/woodproject/image',methods=['POST'])
def update_with_image():
    if 'user_id' not in session:
        return redirect('/logout')
    #Validation of non-image fields:
    if not Woodproject.validate_woodproject(request.form):
        return redirect('/new')
    #Validation of image fields: 
    if 'woodProjectImg' not in request.files:
        flash('No file selected. Upload an image.')
        print("IMAGE VALIDATION - No File Selected")
        return redirect('/edit/<int:id>')
    #Creates the file variable connected to the HTML 
    file = request.files['woodProjectImg']
    if file.filename == '':
        print("IMAGE VALIDATION - File Not Named")
        return redirect('/edit/<int:id>')
    #If image file exists, then save it
    if file:
        print("IMAGE VALIDATION - Start saving file")
        filename = secure_filename(file.filename)
        # image_path = str(UPLOAD_FOLDER)+file.filename
        image_path = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("IMAGE VALIDATION - File saved here:", image_path)
    #Saves the form and the image's path to the db
    data = {
        "project_name": request.form["project_name"],
        "skill_level": request.form["skill_level"],
        "type": request.form["type"],
        "description": request.form["description"],
        "image_path" : image_path,
        "id": request.form["id"]
    }
    Woodproject.update_with_image(data)
    return redirect("/dashboard")




###################################### 
# ROUTE TO DELETE 
###################################### 

@app.route('/destroy/woodproject/<int:id>')
def destory(id):
    if 'user_id' not in session:
        return redirect('logout')
    data = {
        "id":id
    }
    Woodproject.destroy(data)
    return redirect("/dashboard")
