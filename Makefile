run:
	python assignment_server.py

pylint:
	pylint assignment.py

db_upgrade:
	 alembic upgrade head

db_downgrade:
	alembic downgrade -1