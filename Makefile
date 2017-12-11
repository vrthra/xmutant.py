module=example
tries=1
test:
	@mkdir -p .cov
	env  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:src:examples python3 ./src/xmutant.py -a $(tries) $(module)

file=examples/heapsort.py
file=examples/binarysearch.py
file=examples/fact.py
doctest:
	env PYTHONPATH=.:src:examples python3 -m doctest -v $(file)

module:
	env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:src:examples python3 $(file)

clean:
	rm -rf logs/*.log logs/*.log.*

clobber:
	rm -rf logs/*.log logs/*.log.* logs/*.json .cov
