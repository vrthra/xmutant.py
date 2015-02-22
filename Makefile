module=example
test:
	mkdir -p .cov
	@env  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:src:examples ./src/mutant.py $(module)

show:
	@env  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:src:examples ./examples/show.py
