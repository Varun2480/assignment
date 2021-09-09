run:
	python assignment_server.py

pylint:
	pylint assignment.py

db:
	$ alembic upgrade head