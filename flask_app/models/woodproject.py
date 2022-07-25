from multiprocessing import allow_connection_pickling
from operator import truediv
from unittest import result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
#Image upload and validation: 
import os
from werkzeug.utils import secure_filename



class Woodproject:
    db = "woodworking_joint"
    def __init__(self,data):
        self.id = data['id']
        self.project_name = data['project_name']
        self.skill_level = data['skill_level']
        self.type = data['type']
        self.description = data['description']
        self.image_path = data['image_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.liked_by = set() # for number of likes, can just use len({instance}.like_by)
        self.user = None


###################################### 
# SAVE METHODS 
###################################### 

    @classmethod
    def save(cls, data):
        query = "INSERT INTO woodprojects (project_name, skill_level, type, description, image_path, user_id) VALUES (%(project_name)s, %(skill_level)s, %(type)s, %(description)s, %(image_path)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)



###################################### 
# READ METHODS 
###################################### 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM woodprojects;"
        results = connectToMySQL(cls.db).query_db(query)
        all_woodprojects = []
        for row in results:
            all_woodprojects.append(cls(row))
        return all_woodprojects

    @classmethod
    def get_all_with_likes(cls):
        # Standard left join because group by won't work on 
        # specific MYSQL server
        query = "SELECT * FROM woodprojects " \
            "LEFT JOIN favorites on woodprojects.id = "\
            "favorites.woodproject_id; "

        results = connectToMySQL(cls.db).query_db(query)
        if len(results) < 1:
            return None
        project_ids = set()
        projects = []
        for i in range(len(results)):
            this_id = results[i]["id"]
            user_id = results[i]["favorites.user_id"]
            if this_id not in project_ids:    # only create an object if not already done
                project_ids.add(this_id)   # keep track of the projects we've found
                project = cls(results[i])
                if user_id: # check if this exists
                    project.liked_by.add(user_id) # add the id of the user that liked it
                projects.append(project)
            else: # we've already found this project previously
                if projects[-1].id == this_id: # this row likely references the same project in the last row
                    ref_idx = len(projects) - 1
                else:
                    for x in range(len(projects)):  # brute force search otherwise
                        if projects[x].id == this_id:
                            ref_idx = x
                            break
                if user_id:
                    projects[ref_idx].liked_by.add(user_id) # we don't want add a new project, but we do want to add
                                                        # to its liked by
        return projects






    @classmethod
    def get_all_woodprojects_by_one_user(cls,data):
        query = "SELECT * FROM woodprojects WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        all_woodprojects = []
        for row in results:
            all_woodprojects.append(cls(row))
        return all_woodprojects

    @classmethod
    def get_one_woodproject_by_id(cls,data):
        query = "SELECT * FROM woodprojects WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])




###################################### 
# UPDATE METHODS 
###################################### 
    @classmethod
    def update(cls,data):
        query = "UPDATE woodprojects SET project_name=%(project_name)s,skill_level=%(skill_level)s,type=%(type)s,description=%(description)s,updated_at=NOW() WHERE id=%(id)s;"
        print(query)
        # "WHERE id = %(id)s" is coming from the hidden input on edit HTML file
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update_with_image(cls,data):
        query = "UPDATE woodprojects SET project_name=%(project_name)s,skill_level=%(skill_level)s,type=%(type)s,description=%(description)s,image_path=%(image_path)s,updated_at=NOW() WHERE id=%(id)s;"
        print(query)
        # "WHERE id = %(id)s" is coming from the hidden input on edit HTML file
        return connectToMySQL(cls.db).query_db(query,data)


###################################### 
# DELETE METHODS 
###################################### 

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM woodprojects WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


###################################### 
# VALIDATION METHODS 
######################################

    @staticmethod
    def validate_woodproject(woodproject):
        is_valid = True
        if len(woodproject['project_name']) < 3:
            is_valid = False
            flash("Project name must be at least 3 characters","woodproject")
        if "skill_level" not in woodproject:
            is_valid = False
            flash("Please select a skill level","woodproject")
        if "type" not in woodproject:
            is_valid = False
            flash("Please select a type","woodproject")
        if len(woodproject['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","woodproject")
        return is_valid
