from loc.markdown_ltx import MarkdownLtx
from markdown import Markdown

md_ltx=MarkdownLtx()
md=Markdown()

test_str='This is **really** useful _functionality_ for anyone > twelve years'
print "HTML:\n"
print md.convert(test_str)
print "\n"

print "Latex:\n"
print md_ltx.convert(test_str)
print "\n"

test_str=open('datatables/standards/lastds/description', 'r').read()
print "HTML:\n"
print md.convert(test_str)
print "\n"

print "Latex:\n"
print md_ltx.convert(test_str)
print "\n"

