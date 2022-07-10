from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.woodproject import Woodproject
from flask_app.models.user import User


###################################### 
# HOME ROUTE
###################################### 

@app.route('/')
def index():
    return render_template('index.html')


###################################### 
# ROUTE TO DASHBOARD
###################################### 

@app.route('/dashboard')
def results():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_one_by_id(data),woodprojects=Woodproject.get_all())


###################################### 
# ROUTE TO CREATE 
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
    if not Woodproject.validate_woodproject(request.form):
        return redirect('/new')
    data = {
        "project_name": request.form["project_name"],
        "skill_level": request.form["skill_level"],
        "type": request.form["type"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Woodproject.save(data)
    return redirect('/dashboard')


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
# ROUTE TO UPDATE 
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
    return render_template("edit.html", edit=Woodproject.get_one_woodproject_by_id(data), user=User.get_one_by_id(user_data))


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
        "id":session['user_id']
    }
    Woodproject.update(data)
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
