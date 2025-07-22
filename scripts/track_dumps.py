import os
import pandas as pd
from app import db
from app import create_app
from app.models import User, Log, Question, Answer

app = create_app()

# Define export function
def export_database_to_csv():
    # Fixed export directory
    export_dir = os.path.join('deploy', 'data', 'experiment')
    os.makedirs(export_dir, exist_ok=True)

    with app.app_context():
        # Define your tables
        tables = {
            'User': User,
            'Question': Question,
            'Answer': Answer,
            'Log': Log,
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
                df.drop(columns=['_sa_instance_state'], inplace=True, errors='ignore')

            # Export to CSV (overwrite existing files)
            output_path = os.path.join(export_dir, f'{name}.csv')
            df.to_csv(output_path, index=False)

    print(f"Export completed! Files are in: {export_dir}")

if __name__ == "__main__":
    export_database_to_csv()
