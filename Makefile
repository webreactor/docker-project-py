

build: venv/
	venv/bin/pip install -r src/requirements.txt

venv/:
	virtualenv -p python3 venv

clean:
	git clean -f -d -x

