from setuptools import setup

setup(name='pipefy',
      version='0.1',
      description='Unix-like interface for data processing',
      url='http://github.com/storborg/funniest',
      author='Andrew Morozko',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['pipefy'],
      tests_require=['pytest', 'pytest-cov'],
      setup_requires=['pytest-runner'],
      zip_safe=False)
