"""
Extends Markdown with a Latex output type.
"""

from markdown import Markdown, util

ElementTree = util.etree.ElementTree
Comment = util.etree.Comment

class MarkdownLtx(Markdown):

    def __init__(self, *args, **kwargs):
        Markdown.__init__(self, args, kwargs)
        self.serializer=_write_latex
        self.stripTopLevelTags = False

def _serialize_latex(write, elem):
    tag = elem.tag
    text = elem.text
    if tag is Comment:
        write("%% %s\n"%text)
    elif tag is None:
        if text:
            write(text)
        for e in elem:
            _serialize_latex(write,e)
    elif tag=="strong":
        write(r'{\bf')
        write(text)
        for e in elem:
            _serialize_latex(write, e)
        write("}")
    elif tag=="em":
        write(r'\emph{')
        write(text)
        for e in elem:
            _serialize_latex(write, e)
        write("}")
    else:
        write(elem.text)
        for e in elem:
            _serialize_latex(write, e)
    if elem.tail:
        write(elem.tail)

def _write_latex(root):
    assert root is not None
    data = []
    _serialize_latex(data.append, root)
    return " ".join(data)



