help:
	@echo 'Commands:'
	@echo ' lint             - Lint the code with pylint and flake8 and check imports'
	@echo '                    have been sorted correctly'
	@echo ' checkmigrations  - Check whether there are any uncreated migrations' 
	@echo ' test             - Run tests and coverage'
	@echo ' missing          - Run tests, coverage and show which lines are missing'
lint:
	pylint --load-plugins pylint_django *
	flake8
	isort --check-only .
checkmigrations:
	python manage.py makemigrations --dry-run --check
test:
	pytest -v --cov-config .coveragerc --cov
missing:
	pytest -s -vvv --cov-config .coveragerc --cov --cov-report term-missing
