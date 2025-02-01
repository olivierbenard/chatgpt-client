run:
	poetry run python chatgpt_client/client.py

black:
	poetry run black .

mypy:
	poetry run mypy chatgpt_client/

pylint:
	poetry run pylint chatgpt_client/

tests:
	poetry run pytest -vvs --cov=chatgpt_client tests/


checks: black mypy pylint tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
