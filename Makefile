module=example
tries=1
test:
	@mkdir -p .cov
	env  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:xmutant:examples python3 ./xmutant/xmutant.py -a $(tries) $(module)

file=examples/heapsort.py
file=examples/binarysearch.py
file=examples/fact.py
doctest:
	env PYTHONPATH=.:xmutant:examples python3 -m doctest -v $(file)

module:
	env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:xmutant:examples python3 $(file)

clean:
	rm -rf logs/*.log logs/*.log.*

clobber:
	rm -rf logs/*.log logs/*.log.* logs/*.json .cov

pypi:
	python setup.py sdist upload
