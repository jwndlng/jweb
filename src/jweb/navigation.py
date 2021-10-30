"""
    Navigation provides the basic functionality of a page navigation
    to navigate between sites
"""

class Navigation:

    TEMPLATE = 'default/nav.j2'

    def __init__(self, env, pages):
        self._env = env
        self._pages = pages

    def render(self, name, tpl_file=None):

        if tpl_file is None:
            tpl_file = self.TEMPLATE

        # prepare data
        nodes = []
        for page in self._pages:
            node = {
                'href': f"{page['file']}.html",
                'name': page['name'],
                'is_active': False
            }
            if page['name'] == self.page['name']:
                node['is_active'] = True
            nodes.append(node)
        
        # read template
        tpl = self._env.get_template(tpl_file)
        
        # render
        return tpl.render(name=name, nodes=nodes)