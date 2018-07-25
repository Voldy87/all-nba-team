import os
from django import template
register = template.Library()

@register.simple_tag
def i18n_include(template_name, language):
    template_name, extension = os.path.splitext(template_name)
    folder = template_name+"_i18n"
    template_name = '%s/%s.%s%s' % (folder,template_name, language, extension)
    return template.loader.render_to_string(template_name)