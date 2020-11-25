from django import template

register = template.Library()

@register.filter(name= 'getReplies')
def getReplies(dict, comment_pk):
    return dict.get(comment_pk)