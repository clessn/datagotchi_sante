from app.main import bp
from flask import render_template, flash, redirect, url_for, current_app, make_response, g
from flask_login import current_user, login_required
from app.models import User, Log
from flask import request
from app.main.forms import PurchaseForm
from app.auth.forms import Close
from app import db
import pickle


# @bp.before_app_request
# def before_request():
#     pass

@bp.route('/consent')
@login_required
def consent():
    form = PurchaseForm()
    return render_template('main/consent.html', form = form)

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

@bp.route('/lifestyle', methods=["POST"])
@login_required
def lifestyle():
    form = PurchaseForm()
    return render_template('main/lifestyle.html', form = form)

@bp.route('/explain', methods=["POST"])
@login_required
def explain():
    form = PurchaseForm()
    return render_template('main/explain.html', form = form)


@bp.route('/satisfaction', methods=["POST"])
@login_required
def satisfaction():
    form = PurchaseForm()
    return render_template('main/satisfaction.html', form = form)

@bp.route('/intent', methods=["POST"])
@login_required
def intent():
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

