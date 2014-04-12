try:
    from setuptools import setup
except: ImportError:
    from distutils.core import setup

config = {
    'description' : ''
    'author': 'Erin Grant'
    'url': ''
    'download_url': ''
    'author_email': 'e.grant41@gmail.com'
    'version': 0.1
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)

