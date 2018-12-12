# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from accordion.models import AccordionContainer, AccordionTab


@plugin_pool.register_plugin
class AccordionContainerPlugin(CMSPluginBase):
    model = AccordionContainer
    name = 'Accordion'
    render_template = 'accordion/container.html'
    allow_children = True
    child_classes = ['AccordionTabPlugin']

    def render(self, context, instance, placeholder):
        context.update({
            'accordion': instance,
            'placeholder': placeholder,
        })
        return context


@plugin_pool.register_plugin
class AccordionTabPlugin(CMSPluginBase):
    model = AccordionTab
    name = 'Accordion Tab'
    render_template = 'accordion/tab.html'
    allow_children = True
    parent_classes = ['AccordionContainerPlugin']
    require_parent = True

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context
