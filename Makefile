ifeq ($(OS),Windows_NT)
    SEP = \\
else
    SEP = /
endif

clean-python:
	poetry run isort .
	poetry run black .

run-metrics:
	poetry run python code$(SEP)ml$(SEP)metrics.py

run-crossval:
	poetry run python code$(SEP)ml$(SEP)crossval.py

launch-visuals:
	poetry run streamlit run code$(SEP)ml$(SEP)visuals.py
