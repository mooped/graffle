import pystache

def render(template, context):
  with open(template) as t:
    return pystache.render(t.read(), context)
