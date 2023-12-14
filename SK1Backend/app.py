from cs50 import SQL
import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash,generate_password_hash


app = Flask(__name__)

db = SQL("sqlite:///score.db")
app.config.update(SECRET_KEY=os.urandom(24))

@app.route("/", methods=["GET", "POST"])
def index():
    if  request.method == "POST":
      name = request.form.get("name")
      score = request.form.get("score")

      db.execute("INSERT INTO score (name,score) VALUES(?,?)",name,score )
      return redirect("/")

    else:

      score = db.execute("SELECT * FROM score")
      

    return render_template("index.html", score=score)

@app.route("/edit/<id>", methods =["GET","POST"])
def edit_data(id):
  if request.method == "GET":
    editsc = db.execute("SELECT * from score WHERE id = ?",id)[0]
    print(editsc)
    return render_template("edit.html",editsc=editsc)
  elif request.method == "POST":
    editsc_name = request.form.get("name")
    editsc_score = request.form.get("score")
    db.execute("UPDATE score set name = ?, score = ? where id = ?", editsc_name,editsc_score,id)
    return redirect("/")
  
@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    db.execute("DELETE from score where id = ?",id)
    return redirect("/")    

  

@app.route("/register", methods=["GET", "POST"])
def register():
   session.clear()
   """Register user"""
   if request.method == "POST":
      if not request.form.get("username"): 
         return "must provide "
      elif not request.form.get("password"):
         return "must provide password"
      rows = db.execute("SELECT * FROM account WHERE username = ?", request.form.get("username"))

      email = request.form.get("email")
      name = request.form.get("name")
      username = request.form.get("username")
      password = request.form.get("password")
      password_repeat = request.form.get("confirmation")

      hash = generate_password_hash(password)
     
      if len(rows) == 1:
         return "username alredy taken"
      if password == password_repeat:
      
         db.execute("INSERT INTO account (email,name,username,password) VALUES(?,?,?,?)",email,name,username,hash)

         registered_user = db.execute("select * from account where username = ?",username)
         session["user_id"] = registered_user[0]["id"]
         flash('You were successfully registered')
         return redirect("/register")
      else:
         return "must provide matching password"
   else:
      return render_template("register.html")  
   
@app.route("/login",methods=["GET","POST"])
def login():
   session.clear()

   if request.method == "POST":
      if not request.form.get("username"):
         return "must provide username"
      
      elif not request.form.get("password"):
         return "must provide password"
      
      rows = db.execute("SELECT * FROM account WHERE username = ?",request.form.get("username"))

      if len(rows) != 1 or not check_password_hash(rows[0]["password"],request.form.get("password")):
         return "invalid username and/or password"
      
      session["user_id"] = rows[0]["id"]

      return redirect("/")
   
   else:
      return render_template("login.html")
   
@app.route("/logout")
def logout():
   session.clear()

   return redirect("/")
      

      
