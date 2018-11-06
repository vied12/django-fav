build:
	python setup.py sdist

deploy:
	twine upload --skip-existing dist/*
