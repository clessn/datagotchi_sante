ifeq ($(OS),Windows_NT)
    SEP = \\
else
    SEP = /
endif

clean-python:
	poetry run isort .
	poetry run black .

create-features:
	poetry run python code$(SEP)ml$(SEP)feature_engineering.py

score-features:
	poetry run python code$(SEP)ml$(SEP)feature_selection.py

build-sandbox:
	poetry run python code$(SEP)ml$(SEP)sandbox.py

generate-example:
	poetry run python code$(SEP)ml$(SEP)deploy.py generate_questionnaire_and_example

run-crossval:
	poetry run python code$(SEP)ml$(SEP)crossval.py

launch-visuals:
	poetry run streamlit run --client.showSidebarNavigation=False code$(SEP)ml$(SEP)visuals.py

train-best-model:
	poetry run python code$(SEP)ml$(SEP)deploy.py train_best_model
