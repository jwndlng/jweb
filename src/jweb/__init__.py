"""
    JWEB is a simple static website builder to provide an easy
    framework to generate a website based on markdown content
"""

import yaml
import markdown
from jweb.page import Page


class WebApplication:
    
    CONTENT_SEPARATOR = '-----'

    def __init__(self, base_dir, config_file):
        self.base_dir = base_dir
        # Load configuration
        self.load_config(config_file)
        # variables
        self.pages = self._config.get('pages', [])
        # Set paths
        self._raw_content = self.base_dir.joinpath(
            self._config.get('base', {}).get('content', '')
        )

    def load_config(self, config_file):
        if not self.base_dir.joinpath(config_file).exists():
            raise FileNotFoundError(f"Please select a config file that exists. The file {config_file} does not exists!")
        with open(self.base_dir.joinpath(config_file)) as yfile:
            self._config = yaml.safe_load(yfile)
    
    # Render
    def render(self):
        for page in self.pages:

            page_obj = Page(self.base_dir, page, self._config)
            
            # Create folder for subpages
            if page.get('type', '') == Page.CONTENT_TYPE_ARTICLE:
                self.create_folder(page['file'])

            for filepath in self.get_content_pages(page['file']):

                # TODO
                # Two things are important here
                # - Get content to be added on main page
                # - Create subpage if its type article
                title, meta, preview, content = self.parse_markdown_file(filepath)

                if page.get('type', '') == Page.CONTENT_TYPE_ARTICLE:
                    #self.render_subpage(page, filepath)
                    page_obj.add_content(title, meta, preview)
                else:
                    page_obj.add_content(title, meta, content)
            
            if len(page_obj.content) <= 0:
                page_obj.add_content('', '', 'No content found')

            self.create_page(
                page['file'],
                page_obj.render()
            )
                    
        return 0

    def parse_markdown_file(self, filepath):
        state = 0
        title = ''
        preview = ''
        meta = {}
        content = ''
        with open(filepath, 'r', encoding='utf-8') as m_file:
            for line in m_file.readlines():
                if line.strip() == self.CONTENT_SEPARATOR:
                    # States title -> meta data -> content
                    state+=1
                    continue             
                if state == 0:
                    title = line
                elif state == 1:
                    splits = line.split(':')
                    name, value = self.parse_meta(
                                    splits[0].strip(),
                                    splits[1].strip()
                                )
                    meta[name] = value
                elif state == 2:
                    preview += line
                elif state == 3:
                    content += line
                else:
                    raise Exception(f"Reached unknown state {state}")
        return title, meta, preview, markdown.markdown(content)

    def parse_meta(self, name, value):
        if name == 'tags':
            value = value.split(',')
        return name, value

    # Helper
    def create_folder(self, name):
        self.base_dir.joinpath(name).mkdir(exist_ok=True)

    def create_page(self, filepath, content):
        with open(f'{filepath}.html', 'w', encoding='utf-8') as html_file:
            html_file.write(content)

    def get_content_pages(self, name):
        subfolder = self._raw_content.joinpath(name)
        files = subfolder.glob('*.md')
        return files