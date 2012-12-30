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
            write(_ltx_escape(text))
        for e in elem:
            _serialize_latex(write,e)
    elif tag=="a":
        write(text)
    elif tag=="p":
        write("\n")
        if text: write(_ltx_escape(text))
        for e in elem:
            _serialize_latex(write, e)
        write("\n")
    elif tag=="strong":
        write(r'{\bf ')
        write(_ltx_escape(text))
        for e in elem:
            _serialize_latex(write, e)
        write("}")
    elif tag=="em":
        write(r'\emph{')
        write(_ltx_escape(text))
        for e in elem:
            _serialize_latex(write, e)
        write("}")
    else:
        write(_ltx_escape(text))
        for e in elem:
            _serialize_latex(write, e)
    if elem.tail:
        write(_ltx_escape(elem.tail))

def _ltx_escape(text):
    try:
        if "&" in text:
            text = text.replace("&", "\&")
        if "<" in text:
            text = text.replace("<", "$<$")
        if ">" in text:
            text = text.replace(">", "$>$")
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)

def _write_latex(root):
    assert root is not None
    data = []
    _serialize_latex(data.append, root)
    return "".join(data)



