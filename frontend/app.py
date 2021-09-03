from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) 
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'cTask {self.id}>'

@app.route('/do/<int:id>', methods=['POST', 'GET'])
def do(id):
    if requset.method == 'POST':
        task_to_do = Todo.query.get_or_404(id)
        try:
            print('are we doing?')
            task_to_do.done = ~task_to_do.done
            db.session.commmit()
            return redirect('/')
        except Exception as e:
            print(e)
    else:
        tasks = Todo.query.order_by(Todo.data_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.data_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
            
        except Exception as e:
            print(e)
            pass
    else:
        print(request.method)
        return render_template('update.html', tasks=task)

if __name__ == '__main__':
    app.run(debug=True, port=1771)

    content = db.Column(db.String(200), nullable=False) 