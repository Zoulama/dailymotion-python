setup: ##@Install Dependencies
	mkdir ~/.virtualenvs
	python3 -m venv ~/.virtualenvs/dailymotion-python.py
	source ~/.virtualenvs/dailymotion-python.py/bin/activate
	pip install -r requirements.txt
up: ##@Run locally
	docker-compose up --build
down: ##@Stop containers
	docker-compose down
