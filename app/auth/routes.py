from app.auth import bp
from flask import render_template, flash, redirect, url_for, current_app
from app.auth.forms import LoginForm
from flask_login import current_user, login_user, login_required, logout_user
import csv
from app.models import User

CONDITION_ID_LIST = ['explain_A', 'explain_B', 'explain_C']

def get_next_condition_id(user_class, condition_id_list):
    """
    Determines the next condition ID based on the provided criteria.

    Args:
        user_class: The User class instance.
        condition_id_list: A list of condition IDs.

    Returns:
        The next condition ID.

    Raises:
        ValueError: If a condition ID in the list is not valid.
    """

    # Count the number of users for each condition ID
    condition_id_counts = {condition_id: 0 for condition_id in condition_id_list}
    for user in user_class.query.filter(User.condition_id.in_(condition_id_list)).all():
        condition_id_counts[user.condition_id] += 1

    # Check if all condition IDs are valid
    if not all(condition_id in condition_id_counts for condition_id in condition_id_list):
        raise ValueError("Invalid condition ID in the list.")

    # Find the condition ID with the minimum number of users
    min_count = min(condition_id_counts.values())
    min_condition_id_list = [condition_id for condition_id, count in condition_id_counts.items() if count == min_count]

    # Return the first condition ID in the list if there are multiple
    return min_condition_id_list[0]


@bp.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth.login'))   


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(current_app.config['MAIN_PAGE']))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.code.data).first()
        if user.condition_id is None:
            condition_id = get_next_condition_id(User, CONDITION_ID_LIST)
            user.assign_condition(condition_id)
        if user is None :
            flash('Invalid code')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for(current_app.config['MAIN_PAGE']))
    return render_template('auth/login.html', form=form)

@bp.route('/close', methods=['GET', 'POST'])
@login_required
def close():
    logout_user()
    return redirect(url_for('auth.login'))   

@bp.route('/survey', methods=['GET', 'POST'])
def survey():
    return render_template('main/survey.html')



