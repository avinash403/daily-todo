.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete

virtualenv:
	python3 -m venv --prompt '|> todo <| ' env
	env/bin/pip3 install -r requirements-dev.txt
	env/bin/python3 setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

test:
	python3 -m pytest \
		-v \
		--cov=todo \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t todo:latest .

dist: clean
	rm -rf dist/*
	python3 setup.py sdist
	python3 setup.py bdist_wheel

dist-upload:
	twine upload dist/*
