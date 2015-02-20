test:
	mkdir -p .cov
	@env PYTHONPATH=.:src:examples ./src/mutant.py example
