install:

	# Install poetry
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

	# Install poetry dependencies
	~/.poetry/bin/poetry install --without dev

install_dev:
	~/.poetry/bin/poetry install

test:
	isort .
	poetry run python -m pytest .

linter:
	flake8 --exclude=.mypy_cache,.pytest_cache,.run,.venv,.env,.gitignore,Dockerfile,*.txt .

run:
	python3 main.py