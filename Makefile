

build: src/vendor


src/vendor:
	make check-pip
	pip install -r src/requirements.txt

check-pip:
	if [ -z "$(shell which pip)" ]; then easy_install pip; fi;

clean:
	git clean -f -d -x

