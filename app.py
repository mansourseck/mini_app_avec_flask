from flask import Flask, render_template, request, redirect
from db import db
from models import Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        new_title = request.form['title']
        if new_title:
            task.title = new_title
            db.session.commit()
            return redirect('/')
    return render_template('edit.html', task=task)

@app.route('/toggle/<int:id>')
def toggle(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)