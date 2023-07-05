install:

	# Install poetry
	curl -sSL https://install.python-poetry.org | python3 -

	# Install poetry dependencies
	~/.local/bin/poetry install --without dev

install_dev:
	~/.local/bin/poetry install

test:
	isort .
	~/.local/bin/poetry run python -m pytest .

linter:
	flake8 --exclude=.mypy_cache,.pytest_cache,.run,.venv,.env,.gitignore,Dockerfile,*.txt .

run:
	~/.local/bin/poetry run python main.py
	