from flask import Flask, render_template, request, make_response
import pandas as pd
import sqlite3
import csv
from app.models import User, Log, Question, Answer
from app import create_app
from app import db
from dotenv import load_dotenv
from pathlib import Path
import os


app = create_app()

# Load the .env file
load_dotenv()

# Log file
LOG_FILENAME = 'Log.csv'


def display_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(user)


def display_logs():
    with app.app_context():
        logs = Log.query.all()
        for log in logs:
            print(log)


def display_questions():
    with app.app_context():
        questions = Question.query.all()
        for question in questions:
            print(question)

def display_answers():
    with app.app_context():
        answers = Answer.query.all()
        for answer in answers:
            print(answer)

def display_activity():
    with app.app_context():
        for user in User.query.all():
            print(user)
            print("User logs:")
            query = user.logs.select()
            logs = db.session.scalars(query).all()
            for log in logs:
                print(log)

def logs_to_user_status():

    # Load the log file
    track_path = Path(os.getenv("DATA_TRACK_PATH"))
    log_file = track_path / LOG_FILENAME
    log_df = pd.read_csv(log_file, delimiter=",")

    # Convert timestamp to datetime
    log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])

    # For each user, get the last phase they were in and create a dictionary mapping user_id to phase_id
    last_phase = (
        log_df.sort_values('timestamp')
        .groupby('user_id')
        .tail(1)
        .set_index('user_id')['phase_id']
        .to_dict()
    )

    print(last_phase) 
    
    return last_phase