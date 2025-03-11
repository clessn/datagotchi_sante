ifeq ($(OS),Windows_NT)
    SEP = \\
else
    SEP = /
endif

clean-python:
	poetry run isort .
	poetry run black .

create-features:
	poetry run python -c "from app.ml.feature_engineering import feature_engineering; feature_engineering()"

score-features:
	poetry run python -c "from app.ml.feature_selection import feature_selection; feature_selection()"

build-sandbox:
	poetry run python app$(SEP)ml$(SEP)sandbox.py

generate-example:
	poetry run python -c "from app.ml.deploy import deploy; deploy('generate_questionnaire_and_example')"

predict-for-example:
	poetry run python -c "from app.ml.deploy import deploy; deploy('predict_for_example')"

run-crossval:
	poetry run python -c "from app.ml.crossval import run_crossval; run_crossval()"

launch-visuals:
	PYTHONPATH=$(pwd):$PYTHONPATH poetry run streamlit run --client.showSidebarNavigation=False app$(SEP)ml$(SEP)visuals.py

train-best-model:
	poetry run python -c "from app.ml.deploy import deploy; deploy('train_best_model')"

assign-conditions:
	poetry run python -c "from scripts.assign_conditions import assign_conditions; assign_conditions()"

cloud-connect:
	gcloud compute ssh datagotchi

create-model:
	poetry run python -c "from scripts.train_recommender_model import create_recommender_model; create_recommender_model()"

display-users:
	poetry run python -c "from scripts.view_databases import display_users; display_users()"

display-userpiis:
	poetry run python -c "from scripts.view_databases import display_userpiis; display_userpiis()"

display-logs:
	poetry run python -c "from scripts.view_databases import display_logs; display_logs()"

display-questions:
	poetry run python -c "from scripts.view_databases import display_questions; display_questions()"

display-answers:
	poetry run python -c "from scripts.view_databases import display_answers; display_answers()"

display-activity:
	poetry run python -c "from scripts.view_databases import display_activity; display_activity()"

reload-experiment:
	poetry run python -c "from scripts.reload_experiment import reload_databases; reload_databases()"

update-deploy:
	git pull
	sudo supervisorctl stop microapp
	flask db upgrade
	sudo supervisorctl start microapp

start-website:
	poetry run python microapp.py --config=default

debug:
	poetry run python microapp.py --config=debug
