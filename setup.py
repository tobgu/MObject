from setuptools import setup

long_desc = """
MObject is a lightweight library to construct objects and object trees for mocking and stubbing.

It is not meant as a replacement for mock frameworks but rather as a complement.

Installation
-------------

pip install mobject

Documentation
---------------

Available at https://github.com/tobgu/mobject/

Contributing
------------

If you experience problems please log them on GitHub. If you want to contribute code, please fork the
code and submit a pull request.
"""

setup(name='mobject',
      version='0.2.0',
      description='Lightweight library to construct objects and object trees',
      long_description=long_desc,
      url='http://github.com/tobgu/mobject',
      author='Tobias Gustafsson',
      author_email='tobias.l.gustafsson@gmail.com',
      license='LICENCE.mit',
      py_modules=['mobject'],
      use_2to3=True,
      zip_safe=False)