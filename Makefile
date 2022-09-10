help:
	@echo "listen for mqtt"
	@echo "execute configured actions"

version:
	python main.py \
		--version

run:
	python main.py \
		-c main.conf \
		#-q 'mqtt://192.168.1.47:1883/python/mqtttossh/in' \
		#-i 'python/mqtttossh/in' \
		#-o 'python/mqtttossh/out' \
		--debug

log:
	multitail var/log/*

install:
	pip install --no-cache-dir -r requirements.txt
freeze:
	pip freeze > requirements.txt
test-lint:
	pylint $$(git ls-files '*.py')
test-unit:
	pytest
test: test-lint test-unit
