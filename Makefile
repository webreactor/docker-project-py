

build-x: venv/
	# venv/bin/pip install -r src/requirements.txt
	venv/bin/python setup.py install
	# venv/bin/python src/setup.py bdist --format=zip
	@echo "#Run:"
	@echo ". venv/bin/activate"
	@echo "cli.py"
venv/:
	virtualenv -p python3 venv

clean:
	git clean -f -d -x

