from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='placeholder')
def placeholder(value, arg):
    return value.as_widget(attrs={'placeholder': arg})

@register.filter(name='classholder')
def classholder(value, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]
    return value.as_widget(attrs={'class': arg_list[0], 'placeholder': arg_list[1]})
