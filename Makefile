all: generate

init:
	pip install -r requirements.txt

generate:
	pip freeze > requirements.txt
	python defaults_generator.py
	rm -rf dist/*
	pyinstaller --noconfirm pyinstaller.spec