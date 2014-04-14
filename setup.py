try:
    from setuptools import setup
except: ImportError:
    from distutils.core import setup

setup(
    name='DafnyToPythonConverter',
    version='0.1.0',
    author='Erin Grant',
    author_email='e.grant41@gmail.com',
    packages=['translate', 'test_translate'],
    scripts=[],
    url='',
    license='LICENSE.txt',
    description='',
    long_description=open('README.txt').read(),
    install_requires=['nose'],
)
