from app.main import bp
from flask import render_template, flash, redirect, url_for, current_app, make_response, g, send_file, Response
from flask_login import current_user, login_required
from app.models import User, Log, Question, Answer
from flask import request
from app.main.forms import PurchaseForm
from app import db
from app import create_app
import pickle
from datetime import datetime, timezone
import pandas as pd
from app.ml.deploy import predict_for_example
import numpy as np
import matplotlib.pyplot as plt
# Use the Agg backend for non-GUI rendering
import matplotlib
matplotlib.use('Agg')
import io
# Treat multiple answers for checkbox questions
from werkzeug.datastructures import ImmutableMultiDict

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
     # step 1 : extract questions for knowledge
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "knowledge").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content, question.form_id)] = question.get_form()

    return render_template(
        'main/knowledge_before.html',
        questionnaire_dico = questionnaire_dico,
        skip_valid=current_app.config['SKIP_VALID'],
    )

@bp.route('/lifestyle', methods=['GET', 'POST'])
@login_required
def lifestyle():

    # step 1 : extract questions ids for knowledge before
    questionnaire_dico_responses = {}
    questions = Question.query.filter(Question.group_id == "knowledge").all()
    for question in questions:
        questionnaire_dico_responses[(question.question_id, question.question_content, question.form_id)] = question.get_form()
    question_ids = [question_id for question_id, _, _ in questionnaire_dico_responses.keys()]
    
    # step 2 : extract and load answer values for knowledge before
    timestamp = datetime.now(timezone.utc)
    for question_id in question_ids:
        answer_id = request.form[question_id]

        # chose random value if not answered for debug
        if not answer_id and current_app.config['SKIP_VALID']:
            question = db.session.get(Question, question_id)
            answer_id = question.get_random_answer(seed=42).answer_id

        new_log = Log(
            timestamp=timestamp,
            user_id=current_user.user_id,
            question_id=question_id,
            answer_id=answer_id,
            phase_id='knowledge_before'
        )
        db.session.add(new_log)
    db.session.commit()

    # step 3 : extract questions for lifestyle
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "lifestyle").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content, question.form_id)] = question.get_form()

    return render_template(
        'main/lifestyle.html',
        questionnaire_dico = questionnaire_dico,
        skip_valid=current_app.config['SKIP_VALID'],
    )

# Example dictionary
data = {
    'Key1': 0.7,
    'Key2': 0.4,
    'Key3': 0.9,
    'Key4': 0.6,
    'Key5': 0.8,
    'Key6': 0.5
}

@bp.route('/radar_chart', methods=["GET"])
def radar_chart():

    labels = request.args.get('labels').split(',')
    values = [float(value) for value in request.args.get('values').split(',')]

    # Number of variables
    num_vars = len(labels)

    # Compute angle for each category on the radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Make the plot circular by closing the loop
    values += values[:1]
    angles += angles[:1]

    # Initialize the radar chart
    fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(polar=True))

    # Plot the data
    ax.fill(angles, values, color='b', alpha=0.25)
    ax.plot(angles, values, color='b', linewidth=2)

    # Labels and styling
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Save the figure to a bytes buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    
    # Return the image as a response
    return Response(buf.getvalue(), mimetype='image/png')

# Function to transform MultiDict (due to checkbox questions) of the form to a simple dict
def form_todict(request_form):
    form_data = request_form.to_dict(flat=False)
    cleaned_form_data = {}
    for key, value in form_data.items():
        # If [] in the key, it is a checkbox question
        if "[]" in key:
            cleaned_form_data[key.rstrip("[]")] = value
        else:
            cleaned_form_data[key] = value[0]
    return cleaned_form_data


@bp.route('/explain', methods=["POST"])
@login_required
def explain():

    # Convert form from lifestyle with list for questions with multiple answers
    form_data = form_todict(request.form)

    # Dico for prediction
    best_model = current_app.best_model
    selected_features = current_app.selected_features
    lifestyle_dico = {feature: 0.0 for feature in selected_features}

    # step 1 : extract questions for lifestyle
    questionnaire_dico_responses = {}
    questions = Question.query.filter(Question.group_id == "lifestyle").all()
    for question in questions:
        questionnaire_dico_responses[(question.question_id, question.question_content, question.form_id)] = question.get_form()
    
    # step 2 : extract and load answer values for lifestyle
    timestamp = datetime.now(timezone.utc)
    for (question_id, question_content, form_id), questionnaire_value in questionnaire_dico_responses.items():
        
        # For checkbox, result is a list not a value
        if form_id!="checkbox":

            # For cursor, answer_content is registered instead of answerd_id
            if form_id=="cursor":
                answer_content = form_data[question_id]
                # Find the answer_id associated to this answer_content
                for a_id, a_content in questionnaire_value:
                    if a_content == answer_content:
                        answer_id = a_id
            
            else:
                answer_id = form_data[question_id]

            # Chose random value if not answered for debug
            if not answer_id and current_app.config['SKIP_VALID']:
                question = db.session.get(Question, question_id)
                answer_id = question.get_random_answer(seed=42).answer_id
                
            new_log = Log(
                timestamp=timestamp,
                user_id=current_user.user_id,
                question_id=question_id,
                answer_id=answer_id,
                phase_id='lifestyle'
            )
            db.session.add(new_log)

            # Find pilote_id for this question and answer_weight 
            pilote_id = Question.query.filter(Question.question_id == question_id).first().pilote_id
            answer_weight = Answer.query.filter(Answer.answer_id == answer_id).first().answer_weight

            # if scroll, it is a nominal single variable and we have to one-hot encode it
            if form_id=="scroll":
                pilote_id_nominal_single = pilote_id + "_" + str(float(answer_weight))
                if pilote_id_nominal_single in lifestyle_dico:
                    lifestyle_dico[pilote_id_nominal_single] = 1.0
            else:
                if pilote_id in lifestyle_dico:
                    lifestyle_dico[pilote_id] = answer_weight

        # For checkbox, result is a list not a value
        else:
            answers = form_data[question_id]
            for answer_id in answers:
                
                # New log
                new_log = Log(
                timestamp=timestamp,
                user_id=current_user.user_id,
                question_id=question_id,
                answer_id=answer_id,
                phase_id='lifestyle'
                )
                db.session.add(new_log)

                # Add save answer in dico for prediction
                pilote_id = Question.query.filter(Question.question_id == question_id).first().pilote_id
                answer_weight = Answer.query.filter(Answer.answer_id == answer_id).first().answer_weight
                pilote_id_nominal_multiple = pilote_id + "_" + str(int(answer_weight))
                if pilote_id_nominal_multiple in lifestyle_dico:
                    lifestyle_dico[pilote_id_nominal_multiple] = 1.0

    db.session.commit()

    # Convert to dataframe    
    lifestyle_df = pd.DataFrame([lifestyle_dico])
    print(lifestyle_df)

    # Predict
    df_y = predict_for_example(
        df_example = lifestyle_df,
        model_info = (best_model, selected_features),
        is_df_features = True
    )
    predicted_score = df_y['score_tot_prediction'].iloc[0]
    print(predicted_score)

    informative_questions_content_dic = {
        "q1": (
                "How many friends do you have?", 
                "Social connections often provide emotional support and a sense of belonging.",
                50
            ),
        "q2": (
                "How many hours of sleep do you get?",
                "Sleep helps recharge your mind and body, impacting your well-being.",
                30
            ),
        "q3": (
                "How often do you exercise?",
                "Regular exercise reduces stress and boosts your mood.",
                20,
            ),
    }
    explain_dic = {
        "predicted_score": 45,
        "intermediate_predicted_score": 38,
        "n_informative": len(informative_questions_content_dic),
        "informative_questions_content_dic": informative_questions_content_dic,
    }
    form = PurchaseForm()
    return render_template(
        f'main/{current_user.condition_id}.html', 
        form = form,
        explain_dic=explain_dic,
    )


@bp.route('/satisfaction', methods=['GET', 'POST'])
@login_required
def satisfaction():
    # step 1 : extract questions for satisfaction
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "satisfaction").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content, question.form_id)] = question.get_form()

    return render_template(
        'main/satisfaction.html',
        questionnaire_dico = questionnaire_dico,
        skip_valid=current_app.config['SKIP_VALID'],
        )

@bp.route('/intent', methods=['GET', 'POST'])
@login_required
def intent():
    # step 1 : extract questions ids for satisfaction
    questionnaire_dico_responses = {}
    questions = Question.query.filter(Question.group_id == "satisfaction").all()
    for question in questions:
        questionnaire_dico_responses[(question.question_id, question.question_content, question.form_id)] = question.get_form()
    question_ids = [question_id for question_id, _, _ in questionnaire_dico_responses.keys()]
    
    # step 2 : extract and load answer values for satisfaction
    timestamp = datetime.now(timezone.utc)
    for question_id in question_ids:
        answer_id = request.form[question_id]

        # chose random value if not answered for debug
        if not answer_id and current_app.config['SKIP_VALID']:
            question = db.session.get(Question, question_id)
            answer_id = question.get_random_answer(seed=42).answer_id

        new_log = Log(
            timestamp=timestamp,
            user_id=current_user.user_id,
            question_id=question_id,
            answer_id=answer_id,
            phase_id='satisfaction'
        )
        db.session.add(new_log)
    db.session.commit()

    # step 3 : extract questions for intent
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "intent").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content, question.form_id)] = question.get_form()

    return render_template(
        'main/intent.html',
        questionnaire_dico = questionnaire_dico,
        skip_valid=current_app.config['SKIP_VALID'],
        )


@bp.route('/knowledge_after', methods=["POST"])
@login_required
def knowledge_after():
    # step 1 : extract questions ids for intent
    questionnaire_dico_responses = {}
    questions = Question.query.filter(Question.group_id == "intent").all()
    for question in questions:
        questionnaire_dico_responses[(question.question_id, question.question_content, question.form_id)] = question.get_form()
    question_ids = [question_id for question_id, _, _ in questionnaire_dico_responses.keys()]
    
    # step 2 : extract and load answer values for intent
    timestamp = datetime.now(timezone.utc)
    for question_id in question_ids:
        answer_id = request.form[question_id]

        # chose random value if not answered for debug
        if not answer_id and current_app.config['SKIP_VALID']:
            question = db.session.get(Question, question_id)
            answer_id = question.get_random_answer(seed=42).answer_id
            
        new_log = Log(
            timestamp=timestamp,
            user_id=current_user.user_id,
            question_id=question_id,
            answer_id=answer_id,
            phase_id='intent'
        )
        db.session.add(new_log)
    db.session.commit()
    
    # step 3 : extract questions for knowledge
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "knowledge").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content, question.form_id)] = question.get_form()

    return render_template(
        'main/knowledge_after.html',
        questionnaire_dico = questionnaire_dico,
        skip_valid=current_app.config['SKIP_VALID'],
    )


@bp.route('/essaim', methods=["POST"])
@login_required
def essaim():

    # step 1 : extract questions ids for knowledge after
    questionnaire_dico_responses = {}
    questions = Question.query.filter(Question.group_id == "knowledge").all()
    for question in questions:
        questionnaire_dico_responses[(question.question_id, question.question_content, question.form_id)] = question.get_form()
    question_ids = [question_id for question_id, _, _ in questionnaire_dico_responses.keys()]
    
    # step 2 : extract and load answer values for knowledge after
    timestamp = datetime.now(timezone.utc)
    for question_id in question_ids:
        answer_id = request.form[question_id]

        # chose random value if not answered for debug
        if not answer_id and current_app.config['SKIP_VALID']:
            question = db.session.get(Question, question_id)
            answer_id = question.get_random_answer(seed=42).answer_id

        new_log = Log(
            timestamp=timestamp,
            user_id=current_user.user_id,
            question_id=question_id,
            answer_id=answer_id,
            phase_id='knowledge_after'
        )
        db.session.add(new_log)
    db.session.commit()

    # step 3 : extract questions for essaim
    questionnaire_dico = {}
    questions = Question.query.filter(Question.group_id == "essaim").all()
    for question in questions:
        questionnaire_dico[(question.question_id, question.question_content, question.form_id)] = question.get_form()

    return render_template(
        'main/essaim.html',
        questionnaire_dico = questionnaire_dico,
        skip_valid=current_app.config['SKIP_VALID'],
    )

@bp.route('/merci', methods=["POST"])
@login_required
def merci():

    # step 1 : extract questions ids for essaim
    questionnaire_dico_responses = {}
    questions = Question.query.filter(Question.group_id == "essaim").all()
    for question in questions:
        questionnaire_dico_responses[(question.question_id, question.question_content, question.form_id)] = question.get_form()
    question_ids = [question_id for question_id, _, _ in questionnaire_dico_responses.keys()]
    
    # step 2 : extract and load answer values for essaim
    timestamp = datetime.now(timezone.utc)
    for question_id in question_ids:
        answer_id = request.form[question_id]
        new_log = Log(
            timestamp=timestamp,
            user_id=current_user.user_id,
            question_id=question_id,
            answer_id=answer_id,
            phase_id='essaim'
        )
        db.session.add(new_log)
    db.session.commit()

    return render_template('main/merci.html')

