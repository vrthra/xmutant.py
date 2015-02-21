test:
	mkdir -p .cov
	@env  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:src:examples ./src/mutant.py example
