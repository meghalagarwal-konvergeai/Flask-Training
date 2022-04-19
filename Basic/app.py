# Calling Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask starts here
app = Flask(__name__)
# Connecting to SQL Alchemy from creating Database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///mytodo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Defining a Table in a Database
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow) # It is going to create a columns with the date and time on which the data is entered,

    def __repr__(self):
        return f"{self.sno} - {self.title}"

# Creating a function to perform action based on submission
@app.route("/", methods=["GET", "POST"])
# Created a function for Home Page
def home():
    if request.method == "POST": # Checking if there is any entry made by the User to store the data in the table
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()
    allTodos = Todo.query.all()
    return render_template('index.html', alltodo=allTodos) # Returning to index page with or without data.

# Created a function for Updation Page
@app.route("/update/<int:sno>", methods=["GET", "POST"]) # <int:sno> is going to store the Serial Number which is been selected to update from the index.html page
def update(sno):
    if request.method == "POST": # Checking if any updated data sent from Update.html page is submitted and storing in Database
        title = request.form["title"]
        desc = request.form["desc"]        
        new_todo = Todo.query.filter_by(sno=sno).first()
        new_todo.title = title
        new_todo.description = desc
        db.session.add(new_todo)
        db.session.commit()
        return redirect("/") # Returning to Home page after updating in the table.
    update_todo = Todo.query.filter_by(sno=sno).first() # Storing the Serial Number of the row which is selected to update and sendin it to update.html page for updation.
    return render_template("update.html", update_todo=update_todo)

# Created a Delete function
@app.route("/delete/<int:sno>") # <int:sno> is going to store the Serial Number which is been selected to delete from the index.html page
def delete(sno):
    delete_todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect("/") # Redirecting back to Home Page

# Program Starts Here
if __name__ == "__main__":
    app.run(debug=True)