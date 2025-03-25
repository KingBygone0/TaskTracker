from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Route: Homepage (View Tasks)
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Route: Add Task
@app.route('/add', methods=['POST'])
def add_task():
    description = request.form['description']
    due_date = request.form['due_date']
    new_task = Task(description=description, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Route: Mark Task as Complete
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.completed = True
    db.session.commit()
    return redirect(url_for('index'))

# Route: Delete Task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Initialize database
with app.app_context():
    db.create_all()

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
@app.route("/")
def home():
    return "Welcome to Task Tracker!"

