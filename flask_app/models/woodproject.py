from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Woodproject:
    db = "woodworking_joint"
    def __init__(self,data):
        self.id = data['id']
        self.project_name = data['project_name']
        self.skill_level = data['skill_level']
        self.type = data['type']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = user.User.get_one_by_id({'id':self.user_id}) #This pulls in the user who created each work project


###################################### 
# CREATE METHODS 
###################################### 

    @classmethod
    def save(cls, data):
        query = "INSERT INTO woodprojects (project_name, skill_level, type, description, user_id) VALUES (%(project_name)s, %(skill_level)s, %(type)s, %(description)s, %(user_id)s);"
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
            print(row['type']) #TODO: Double check this. From "SHows" it was "release_date". Temp change to "type"
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
