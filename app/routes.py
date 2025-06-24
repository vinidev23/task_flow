from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Task
from . import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    tarefas = Task.query.filter_by(user_id = current_user.id).order_by(Task.due_date).all()
    return render_template('dashboard.html', tarefas = tarefas)

@main.route('/nova', methods=['GET', 'POST'])
@login_required
def nova_tarefa():
    if request.method == 'POST':
        titulo = request.form['title']
        descricao = request.form['description']
        status = request.form['status']
        data_entrega = request.form['due_date']
        
        if data_entrega:
            try:
                data_entrega = datetime.strptime(data_entrega, '%Y-%m-%d').date()
            except ValueError:
                flash('Data inválida')
                return redirect(url_for('main.nova_tarefa'))
        else:
            data_entrega = None
        
        nova = Task(
            title=titulo,
            description=descricao,
            status=status,
            due_date=data_entrega,
            user_id=current_user.id
        )
        
        db.session.add(nova)
        db.session.commit()
        flash('Tarefa criada com sucesso!')
        return redirect(url_for('main.dashboard'))

    return render_template('nova_tarefa.html')

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id):
    tarefa = Task.query.get_or_404(id)
    
    if tarefa.user_id != current_user.id:
        flash("Você não tem permissão para editar esta tarefa.")
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        tarefa.title = request.form['title']
        tarefa.description = request.form['description']
        tarefa.status = request.form['status']
        data_entrega = request.form['due_date']
        
        if data_entrega:
            try:
                tarefa.due_date = datetime.strptime(data_entrega, '%Y-%m-%d').date()
            except ValueError:
                flash('Data inválida')
                return redirect(url_for('main.editar_tarefa', id = id))
        else:
            tarefa.due_date = None
            
        db.session.commit()
        flash('Tarefa editada com sucesso!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('editar_tarefa.html', tarefa = tarefa)


@main.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_tarefa(id):
    tarefa = Task.query.get_or_404(id)
    
    if tarefa.user_id != current_user.id:
        flash("Você não tem permissão para excluir essa tarefa.")
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(tarefa)
    db.session.commit()
    flash('Tarefa excluída com sucesso!')
    return redirect(url_for('main.dashboard'))