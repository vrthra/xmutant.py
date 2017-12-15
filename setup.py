from setuptools import setup

setup(name='xmutant',
      version='0.3',
      description='The python3 bytecode based mutation analysis framework',
      long_description="""
This package provides a byte-code based mutation analysis framework for Python. It computes the mutation score (The quality score) of your doctests. Bytecode based mutation analysis ensures that invalid mutants are completely avoided (unlike source code based mutants), and also that trivial redundant and equivalent mutants (that can be distinguished by compiler) are already removed.  It uses coverage analysis to ensure that only covered mutants that have a chance to be detected are run. It also includes randomized evaluation of equivalent mutants (use -a to set the number of attempts to be made).

        Compatibility
        -------------
        It was tested on Python 3.6
        
        
        To run
        ------
        
          python xmutant.py -a <attempts> <module to be tested>
        
        Mutation Operators (on bytecode)
        --------------------------------
        
        - modify constants
        - replace boolean comparators (< <= == != > >=)
        - replace arithmetic operators (+ - * / // ./. ** % << >> ^)
        - remove unary negation and invert
        - invert unary signs
        - swap 'and' and 'or' in boolean expressions
        - swap inplace 'and' and 'or' in assignments
        - swap 'jump if * or pop' and 'jump if * and pop'
        - swap 'pop if true' and 'pop if false'      
      
""",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
      ],
      keywords='mutation-testing mutation-analysis',
      url='http://github.com/vrthra/xmutant.py',
      author='Rahul Gopinath',
      author_email='rahul@gopinath.org',
      license='GPLv3',
      packages=['xmutant'],
      zip_safe=False)
