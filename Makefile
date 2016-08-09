
entry:
	if [ -n "$(IN_DOCKER)" ]; then \
		make build-all; \
	else \
		make docker-build; \
	fi;

docker-build:
	docker build --tag=docker-project .
	docker run -ti -v $(shell pwd):/opt -w /opt -e IN_DOCKER=true docker-project make

build-all: clean venv/
	venv/bin/pip install -r requirements.txt
	venv/bin/python setup.py install
	venv/bin/pyinstaller docker-project.spec
	chmod a+w dist -R
	@echo "binary is here:"
	@echo "dist/docker-project"

venv/:
	virtualenv -p python3.4 venv

clean:
	git clean -f -d -x

