.PHONY: install run test

install:
	python3 -m venv env
	. env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	. env/bin/activate && python app.py

test:
	. env/bin/activate && python -m unittest discover -s . -p "test_app.py"
