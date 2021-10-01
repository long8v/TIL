from flask import Flask, render_template, url_for, request, redirect
from datetime import *
from redis.sentinel import Sentinel
from redis import *
from app import app, redis_client, Todo, db
from datetime import timedelta

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
    sentinel = Sentinel([('127.0.0.1', 23679), ('127.0.0.1', 23680), 
                        ('127.0.0.1', 26381)], 
                        socket_timeout=app.config["REDIS_SOCKET_TIMEOUT"])

    master = sentinel.master_for('mymaster')
    slave = sentinel.slave_for('mymaster') 
    if not redis_client.hexists(12, 'log'):
    # if not master.hexists(12, 'log'):
        print('there is no log') 
        # master.hset(12, 'log', 0) 
        redis_client.hset(12, 'log', 0)
        redis_client.expire(12, timedelta(seconds=app.config["REDIS_EXPIRE_TIME"]))

    if request.method == 'POST':
        # log = int(master.hget(12, 'log'))
        log = int(redis_client.hget(12, 'log'))
        log += 1 
        
        print(f'{log}th todo list')
        # master.hset(12, 'log', log)
        print(app.config["REDIS_EXPIRE_TIME"])
        redis_client.hset(12, 'log', log)
        redis_client.expire(12, timedelta(seconds=app.config["REDIS_EXPIRE_TIME"]))

        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as E:
            return f'There was an issue adding your task\n{E}'
    # log key
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
    app.run(debug=True, host='0.0.0.0', port=8080)
    content = db.Column(db.String(200), nullable=False) 