.PHONY: install run test

install:
	pip install --upgrade pip && pip install -r requirements.txt

run:
	python app.py

test:
	python -m unittest discover -s . -p "test_app.py"
