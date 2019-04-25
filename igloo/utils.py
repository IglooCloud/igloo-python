from datetime import datetime


def get_from_dict(d, keys):
    if len(keys) == 0:
        return d
    else:
        return get_from_dict(d[keys[0]], keys[1:])


def parse_arg(arg_name, arg_value):
    if arg_value is None:
        return ""
    else:
        return "%s:%s" % (arg_name, get_representation(arg_value))


def get_representation(arg_value):
    if arg_value is None:
        return ""
    elif isinstance(arg_value, str):
        return '"%s"' % arg_value
    elif isinstance(arg_value, bool):
        return "true" if arg_value else "false"
    elif isinstance(arg_value, datetime):
        return '"%s"' % arg_value.isoformat()
    elif isinstance(arg_value, dict):
        parsed_items = []
        for key, value in arg_value.items():
            parsed_items.append('"%s":%s' % (key, get_representation(value)))

        return "{%s}" % ",".join(parsed_items)
    else:
        return str(arg_value)
