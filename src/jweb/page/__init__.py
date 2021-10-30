"""
    Page package provides multiple types of web pages like simple content page
    or articles with a detail page. Depending on the type different rendering
    will be choosen.
"""

from jinja2 import Environment, FileSystemLoader
from jweb.navigation import Navigation
from jweb.settings import TEMPLATE_DIR

class Page:

    CONTENT_TYPE_DEFAULT = 'default'
    CONTENT_TYPE_ARTICLE = 'article'
    PTYPE_MAIN = 1
    PTYPE_CONTENT = 2
    NAV_MAIN = 'main'
    NAV_FOOTER = 'footer'

    DEF_TPL = 'default/default.j2'
    SOCIAL_MEDIA_TPL = 'default/social_media.j2'
    SOCIAL_MEDIA_HEADER_TPL = 'default/social_media_header.j2'


    def __init__(self, page, config, page_type=PTYPE_MAIN, params={}):
        self.tpl_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        self.page = page
        self.pages = config.get('pages', [])
        self.social_media = config.get('social_media', {})
        self.type = page_type
        self.params = {
            'meta': {
                'author': config['base']['author'],
                'description': ''
            }
        }
        self.content = []

    def add_content(self, title, meta, content):
        self.content.append({
            'title': title,
            'meta': meta,
            'content': content
        })

    def get_params(self):
        params = self.params
        params['print_content'] = self.render_content()
        params['print_main_navigation'] = self.render_nav(
            "main",
            [p for p in self.pages if self.NAV_MAIN in p['nav']]
        )
        params['print_foot_navigation'] = self.render_nav(
            "foot",
            [p for p in self.pages if self.NAV_FOOTER in p['nav']]
        )
        params['print_social_media'] = self.render_social_media()
        params['print_social_media_header'] = self.render_social_media(
            tpl_file=self.SOCIAL_MEDIA_HEADER_TPL
        )
        params['title'] = self.page['title']
        return params

    def render(self):
        params = self.get_params()
        tpl = self.tpl_env.get_template(self.DEF_TPL)
        return tpl.render(**params)

    def render_content(self):
        if self.page['type'] == self.CONTENT_TYPE_DEFAULT:
            return self.render_overview()
        elif self.page['type'] == self.CONTENT_TYPE_ARTICLE:
            if self.type == self.PTYPE_MAIN:
                return self.render_article_overview()
            else:
                return self.render_article()

    def render_overview(self):
        tpl = self.tpl_env.get_template('page_default.j2')
        return tpl.render(content=self.content)

    def render_article_overview(self):
        tpl = self.tpl_env.get_template('page_article_overview.j2')
        return tpl.render(content=self.content)

    def render_article(self):
        tpl = self.tpl_env.get_template('page_article_detail.j2')
        return tpl.render(content=self.content)

    def render_nav(self, name, pages):
        """
        Creates a navigation and renders it

        :returns: rendered html template as string
        """
        nav = Navigation(self._env, pages)
        return nav.render()

    def render_social_media(self, tpl_file=None):

        if tpl_file is None:
            tpl_file = self.SOCIAL_MEDIA_TPL

        # read template
        tpl = self.tpl_env.get_template(tpl_file)
        # render
        return tpl.render(social_media=self.social_media)