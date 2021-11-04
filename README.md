# jweb

JWEB is a static web application builder using Jinja Template Engine for the rendering.
The idea is to have a very simple website management using a config file and writing markdown.

## Configuration

The configuration file needs to contain the following settings:
```YAML
---
base:
  author: Max Mustermann
  contact: max.mustermann@demo.com
  timezone: 'Europe/Zurich'
  content: raw # In which subdirectory it will find the raw markdown files
pages:
  - file: index
    name: 'About'
    nav: [main]
    title: 'Welcome to jwndlng.github.io!'
    type: default
  - file: posts
    name: 'My Posts'
    nav: [main]
    title: 'Posts' # Pagetitle h1
    type: article # (default | article)
  - file: about-this-website
    name: 'About this Website'
    nav: [footer]
    title: 'About this Website'
    type: default
templates:
  nav: nav
  article: page_article
  default: default
social_media:
  github:
    title: GitHub
    href: https://github.com/max.mustermann
  gitlab:
    title: GitLab
    href: https://gitlab.com/max.mustermann
  linkedin:
    title: LinkedIn
    href: https://linkedin.com/in/max.mustermann
```

## Build

To build the python package

1. Create a virtuel env and install the requirements
2. Enter the python venv

```
. .venv/bin/activate
```

2. Build the package
```
python -m pip install --upgrade build 
python -m build 
```

Now you can use the wheel file and install it on your webapplication project using pip!

```
pip install path/to/jweb_pkg_jwndlng-0.1.0-py3-none-any.whl 
```

## Usage

Provide a python file including the package and referencing the config file is sufficient to generate the website.
The following code shows a simple implementation
```python
import pathlib
from jweb import WebApplication

BASE_DIR = pathlib.Path(__file__).parent.absolute()

app = WebApplication(BASE_DIR, BASE_DIR.joinpath('config.yml'))
app.render()
``` 