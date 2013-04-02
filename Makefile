module=tests

test:
	@nosetests --stop --with-coverage --cover-package=elasticfun \
		--cover-branches --cover-inclusive --verbosity=2 -s $(module) && \
		steadymark

deps:
	@pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete
	rm -rf .coverage

publish:
	@# NOTE: remember to change the version on setup.py before publishing
	@python setup.py sdist upload
