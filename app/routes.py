from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Task
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    tarefas = Task.query.filter_by(user_id = current_user.id).order_by(Task.due_date).all()
    return render_template('dashboard.html', tarefas = tarefas)