from flask import Flask, Blueprint, render_template, request, redirect, jsonify
from models import Task

app = Blueprint('app', __name__)  # Use Blueprint

@app.route('/')
def index():
    tasks = Task.get_all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    Task.add(request.form['title'])
    return redirect('/')

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    Task.update(task_id, request.json['completed'])
    return jsonify({'success': True})

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    Task.delete(task_id)
    return jsonify({'success': True})
