from setuptools import setup
import os
import codecs
import re


install_requires = ['aiohttp>=3.0.1']
extras_require = {
    'aioredis': ['aioredis>=1.0.0'],
}


with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'aiohttp_session', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')
def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()

setup(name='aiohttp-session',
      version=version,
      description=("only for maxwin aiohttp session"),
      long_description='\n\n'.join((read('README.md'))),
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: AsyncIO',
      ],
      author='candy',
      author_email='hfcandyabc@163.com',
      url='',
      license='Apache 2',
      packages=['mw_aiohttp_session'],
      python_requires=">=3.5",
      install_requires=install_requires,
      include_package_data=True,
      extras_require=extras_require)