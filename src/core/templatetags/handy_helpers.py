from django.template import Library


register = Library()

TAG_TO_BOOTSTRAP = {
    'error': 'danger',
}


def convert_tag(tag):
    if tag in TAG_TO_BOOTSTRAP:
        return TAG_TO_BOOTSTRAP[tag]
    else:
        return tag


@register.filter
def message_bootstrap_class_str(message):
    return ' '.join(
        'alert-' + convert_tag(tag) for tag in message.tags.split(' ')
    )
