
from report import LocReport
from loc_markdown.markdown_ltx import MarkdownLtx
from loc_markdown.superscript  import SuperscriptExtension
from sys import stdout
import os
import re
from tempfile import NamedTemporaryFile
from string import maketrans, Template

ltx_special_chars=maketrans(r'_$^&', "----")

class LatexTemplate(Template):
    delimiter='\subst'

def should_cleanup():
    try:
        if os.environ['CLEANUP'] == 'no':
            return False
        else:
            return True
    except KeyError:
        return True

# cleanup
def cleanup(fname):
    if should_cleanup():
        try:
            os.remove(fname)
        except OSError:
            pass

md=MarkdownLtx(extensions=[SuperscriptExtension()])

class LabbReport(LocReport):

    @staticmethod
    def sanitize(str):
        return re.sub('([$#&^\%_])',r'\\\1',str)

    def _markdown_convert(self, string):
        return md.convert(string)

    def _render_sample_info(self, values={}):
        def maybe_include(prefix, key):
            if key in values and values[key] and values[key].strip() != '':
                return "\item " + prefix + ": " + values[key].strip() + "\n"
            else:
                return ""

        return maybe_include("Sample identifying name", 'samplename') \
            + maybe_include("Date sample was taken", 'sampledate') \
            + maybe_include("Location sample was taken", 'samplelocation')

    def generate_tex(self, fh=stdout):

        template_file=open(os.path.join('loc_app', 'templates','report','pdf','labb.tex'))
        template = LatexTemplate(template_file.read())
        template_file.close()

        user=""
        if self.user('first'):  user = 'For ' + self.user('first')
        if self.user('second'): user = user + r'\\ ' + self.user('second')

        values = {
            'user':             user,
            'inunits':          self.units('in_rep'),
            'outunits':         self.units('out_rep'),
            'longinunits':      self.units('in_long'),
            'longoutunits':     self.units('out_long'),
            'sampleinfo':       self._render_sample_info({
                    'samplename':       self.sample()['name'],
                    'sampledate':       self.sample()['date'],
                    'samplelocation':   self.sample()['location'],
                    }),
            'resultssection':   self._results_section(),
            'unitssection'  :
                'units' in self._text_options
                and r'\unitssection'
                or  r'\relax',
            'standardssection':
                'levels' in self._text_options
                and r'\standardssection'
                or  r'\relax',
            'standardblurbs': self._standards_blurbs()
        }
        print >>fh, template.substitute(values)

    def _standards_blurbs(self):
        result = ''
        for standard in self.standards():
            description = self.standards()[standard].description()
            if description is not None:
                result += '\item ' + md.convert(description)
            else:
                result += '\item ' + standard + ': description not available'
        return result

    def generate(self):
        image_dir = os.path.join(os.getcwd(), 'loc_app', 'data', 'media')
        try:
            texinputs_env=os.environ['TEXINPUTS']
        except KeyError:
            texinputs_env=""
        os.environ["TEXINPUTS"]=image_dir + ":" + texinputs_env
            
        outfile=NamedTemporaryFile(delete=should_cleanup(),suffix=".tex")

        self.generate_tex(outfile)
        outfile.flush()
        doc_dir=os.path.dirname(outfile.name)
        saved_dir=os.getcwd()
        os.chdir(doc_dir)
        self._pdflatex_stat=os.system("pdflatex -interaction nonstopmode " + outfile.name + ">& /dev/null")
        doc_basename=os.path.splitext(outfile.name)[0]
        os.chdir(saved_dir)

        cleanup(doc_basename + '.aux')

        if self._pdflatex_stat:
            return doc_basename + '.log'
        else:
            cleanup(doc_basename + '.log')
            return doc_basename + '.pdf'

    def http_headers(self):
        username = self.user('first')
        if self.user('second'): username = username + '_' + self.user('second')
 
        if self._pdflatex_stat:
            return {"Content-type": "text/plain"}
        else:
            return {"Content-type":        "application/pdf",
                    "Content-disposition": "attachment; filename=LABB-%s.pdf" % username}
 

    

