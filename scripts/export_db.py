import os
from datetime import datetime

import pandas as pd

from app import create_app, db
from app.models import Answer, Log, Question, User

app = create_app()


def export_database_to_csv(export_dir=None):
    """
    Export the database tables to CSV files.
    :param export_dir: The directory where CSV files will be saved.
                       If None, defaults to ('deploy/data/experiment/<timestamp>')
    """
    # Default export_dir
    if export_dir is None:
        now = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        export_dir = os.path.join("deploy", "data", "experiment", now)

    os.makedirs(export_dir, exist_ok=True)

    with app.app_context():
        tables = {
            "User": User,
            "Question": Question,
            "Answer": Answer,
            "Log": Log,
        }

        for name, table in tables.items():
            if isinstance(table, db.Table):
                # For association tables
                query = db.session.execute(table.select())
                df = pd.DataFrame(query.fetchall(), columns=query.keys())
            else:
                # For models
                query = table.query.all()
                df = pd.DataFrame([row.__dict__ for row in query])
                df.drop(columns=["_sa_instance_state"], inplace=True, errors="ignore")

            output_path = os.path.join(export_dir, f"{name}.csv")
            df.to_csv(output_path, index=False)

    print(f"Export completed! Files are in: {export_dir}")
