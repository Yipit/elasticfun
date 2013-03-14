test:
	nosetests --with-coverage --cover-package=elasticfun --verbosity=2 -s tests

install:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete
	rm -rf .coverage
