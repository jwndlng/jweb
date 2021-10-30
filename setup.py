
from setuptools import setup

setup(
    name='jweb-pkg-jwndlng',
    author = 'Jan Wendling',
    author_email = 'jan.wendling@gmail.com',
    description = 'JWEB is a static web application builder used for hostings like github.io',
    url = 'https://github.com/jwndlng/jweb',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=['jweb'],
    install_requires = [
        'docutils>=0.17.1',
        'Jinja2>=3.0.1',
        'Markdown>=3.3.4',
        'MarkupSafe>=2.0.1',
        'PyYAML>=5.4.1'
    ]
)
