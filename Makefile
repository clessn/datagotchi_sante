ifeq ($(OS),Windows_NT)
    SEP = \\
else
    SEP = /
endif

clean-python:
	poetry run isort .
	poetry run black .

create_features:
	poetry run python code$(SEP)ml$(SEP)feature_engineering.py

run-crossval:
	poetry run python code$(SEP)ml$(SEP)crossval.py
