from app.main import bp
from flask import render_template, flash, redirect, url_for, current_app, make_response, g
from flask_login import current_user, login_required
from app.models import User, Log, Question, Answer
from flask import request
from app.main.forms import PurchaseForm
from app import db
from app import create_app
import pickle
from datetime import datetime, timezone

# @bp.before_app_request
# def before_request():
#     pass

@bp.route('/consent')
@login_required
def consent():
    return render_template('main/consent.html')

@bp.route('/knowledge_before', methods=["POST"])
@login_required
def knowledge_before():
    form = PurchaseForm()
    return render_template('main/knowledge_before.html', form = form)

@bp.route('/knowledge_after', methods=["POST"])
@login_required
def knowledge_after():
    form = PurchaseForm()
    return render_template('main/knowledge_after.html', form = form)

@bp.route('/lifestyle', methods=['GET', 'POST'])
@login_required
def lifestyle():
    # step 1 : extract questions for lifestyle
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "lifestyle").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content, question.form_id)] = question.get_form()

    return render_template('main/lifestyle.html', questionnaire_dico = questionnaire_dico)

@bp.route('/explain', methods=["POST"])
@login_required
def explain():
    # step 1 : extract questions for lifestyle
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "lifestyle").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content, question.form_id)] = question.get_form()
    
    # step 2 : extract and load answer values for lifestyle
    timestamp = datetime.now(timezone.utc)
    for (question_id, question_content, form_id), questionnaire_value in questionnaire_dico.items():
        # For cursor, answer_content is registered instead of answerd_id
        if form_id=="cursor":
            answer_content = request.form[question_id]
            # Find the answer_id associated to this answer_content
            for a_id, a_content in questionnaire_value:
                if a_content == answer_content:
                    answer_id = a_id
        else:
            answer_id = request.form[question_id]
        new_log = Log(
            timestamp=timestamp,
            user_id=current_user.user_id,
            question_id=question_id,
            answer_id=answer_id,
            phase_id='lifestyle'
        )
        db.session.add(new_log)
    db.session.commit()

    form = PurchaseForm()
    return render_template(f'main/{current_user.condition_id}.html', form = form)


@bp.route('/satisfaction', methods=['GET', 'POST'])
@login_required
def satisfaction():
    # step 1 : extract questions for satisfaction
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "satisfaction").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content)] = question.get_form()
        
    return render_template('main/satisfaction.html', questionnaire_dico = questionnaire_dico)

@bp.route('/intent', methods=['GET', 'POST'])
@login_required
def intent():
    # step 1 : extract questions ids for satisfaction
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "satisfaction").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content)] = question.get_form()
    question_ids = [question_id for question_id, _ in questionnaire_dico.keys()]
    
    # step 2 : extract and load answer values for satisfaction
    timestamp = datetime.now(timezone.utc)
    for question_id in question_ids:
        answer_id = request.form[question_id]
        new_log = Log(
            timestamp=timestamp,
            user_id=current_user.user_id,
            question_id=question_id,
            answer_id=answer_id,
            phase_id='satisfaction'
        )
        db.session.add(new_log)
    db.session.commit()

    form = PurchaseForm()
    return render_template('main/intent.html', form = form)

@bp.route('/essaim', methods=["POST"])
@login_required
def essaim():
    form = PurchaseForm()
    return render_template('main/essaim.html', form = form)

@bp.route('/merci', methods=["POST"])
@login_required
def merci():
    form = PurchaseForm()
    return render_template('main/merci.html', form = form)

