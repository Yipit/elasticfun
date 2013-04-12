# Variables you might need to change in the first place
#
# This is probably the only section you'll need to change in this Makefile.
# Also, make sure you don't remove the `<variables/>' tag. Cause those marks
# are going to be used to update this file automatically.
#
# <variables>
PACKAGE=elasticfun
CUSTOM_PIP_INDEX=
# </variables>

all: unit functional steadymark

unit:
	@make run_test suite=unit

functional:
	@make run_test suite=functional

run_test:
	@if [ -d tests/$(suite) ]; then \
		echo "Running \033[0;32m$(suite)\033[0m test suite"; \
		make prepare; \
		nosetests --stop --with-coverage --cover-package=$(PACKAGE) \
			--cover-branches --verbosity=2 -s tests/$(suite); \
	fi

steadymark:
	@hash steadymark &> /dev/null && steadymark; echo  # This echo tells the shell that everything worked

prepare: clean install_deps build_test_stub

install_deps:
	@if [ -z $$SKIP_DEPS ]; then \
		echo "Installing missing dependencies..."; \
		[ -e requirements.txt ] && pip install -r requirements.txt &> .build.log; \
		[ -e development.txt  ] && pip install -r development.txt  &> .build.log; \
	fi

build_test_stub:
	@python setup.py build
	@find ./build -name '*.so' -exec mv {} tests/unit \;

clean:
	@find . -name '*.pyc' -delete
	@python setup.py clean
	@rm -rf .coverage dist *.log

publish:
	@# NOTE: remember to change the version on setup.py before publishing
	@python setup.py sdist upload
