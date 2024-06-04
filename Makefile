clean-python:
	isort .
	black .

run-metrics:
	poetry run python code\ml\metrics.py

run-crossval:
	poetry run python code\ml\crossval.py