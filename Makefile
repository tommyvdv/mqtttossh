help:
	@echo "listen for mqtt"
	@echo "execute configured actions"

version:
	python main.py --version

run:
	python main.py -q 'mqtt://192.168.1.47:1883/python/mqtttossh/in' \
		--debug

install:
	pip install --no-cache-dir -r requirements.txt
freeze:
	pip freeze > requirements.txt
test-lint:
	pylint main.py main.conf src
test-unit:
	python -m unittest
test: test-lint test-unit
