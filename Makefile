module=example
test:
	mkdir -p .cov
	@env  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:src:examples ./src/mutant.py $(module)

file=examples/fact.py
doctest:
	python -m doctest -v $(file)

clean:
	rm -rf logs/*.log
