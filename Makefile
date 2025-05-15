# Note: pylint might fail due to type annotation issues
install:
	pip install -r requirements.txt

lint:
	pylint --disable=R,C main.py

test:
	python -m pytest -vv --cov=main test_ride_system.py
