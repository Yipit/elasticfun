test:
	nosetests --stop --with-coverage --cover-package=elasticfun \
		--cover-branches --verbosity=2 -s tests && \
	steadymark

deps:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete
	rm -rf .coverage
