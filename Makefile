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

run-crossval:
	poetry run python code$(SEP)ml$(SEP)crossval.py

launch-visuals:
	poetry run streamlit run code$(SEP)ml$(SEP)visuals.py
