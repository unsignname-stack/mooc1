
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView

BUILDIN_STYLES = {
    'default': 'xadmin/includes/sitemenu_default.html',
    'accordion': 'xadmin/includes/sitemenu_accordion.html',
    'self_default': 'xadmin/includes/self_sitemenu_default.html',
    'self_accordion': 'xadmin/includes/self_sitemenu_accordion.html',

}


class SiteMenuStylePlugin(BaseAdminPlugin):

    menu_style = None

    def init_request(self, *args, **kwargs):
        return bool(self.menu_style) and self.menu_style in BUILDIN_STYLES

    def get_context(self, context):
        context['menu_template'] = BUILDIN_STYLES[self.menu_style]
        return context

site.register_plugin(SiteMenuStylePlugin, CommAdminView)
