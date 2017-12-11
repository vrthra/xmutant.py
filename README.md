Use opcodes from
http://unpyc.sourceforge.net/Opcodes.html
https://blog.visucore.com/2011/5/4/python-bytecode-archeology

The python 3.6 bytecode based mutation analysis framework

It also implements a partial mutant equivalence detector based on random
sampling.

Interface for only `doctests` are implemented.

# Usage

Ensure that your `doctest` test cases pass. Then execute

```
python3 ./xmutant/xmutant.py -a <tries> <module>
```

where tries is the number of random samples to be used to attempt to kill any
mutant that is not killed by any given test cases.
