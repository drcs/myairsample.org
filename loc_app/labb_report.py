
from report import LocReport
from markdown.markdown_ltx import MarkdownLtx
from markdown.superscript import SuperscriptExtension
from sys import stdout
import os
from tempfile import NamedTemporaryFile
from string import maketrans, Template

ltx_special_chars=maketrans(r'_$^&', "----")

class LatexTemplate(Template):
    delimiter='\subst'

md=MarkdownLtx(extensions=[SuperscriptExtension()])

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

def ltx_tr(xs):
    return str.join(' & ',map(str,xs)) + r'\\'

class LabbReport(LocReport):

    def generate_tex(self, fh=stdout):

        template_file=open(os.path.join('loc_app', 'templates','report','pdf','labb.tex'))
        template = LatexTemplate(template_file.read())
        template_file.close()

        user=""
        if self.user('first'):  user = 'For ' + self.user('first')
        if self.user('second'): user = user + r'\\ ' + self.user('second')
        user=str(user).translate(ltx_special_chars)

        values = {
            'user':             user,
            'inunits':          self.units('in_rep'),
            'outunits':         self.units('out_rep'),
            'longinunits':      self.units('in_long'),
            'longoutunits':     self.units('out_long'),
            'samplename':       self.sample()['name'],
            'sampledate':       self.sample()['date'],
            'samplelocation':   self.sample()['location'],
            'resultssection':   self._results_section()
        }
        print >>fh, template.substitute(values)

        fh_null = open('/dev/null', 'w')

        # Standards descriptions
        print >>fh_null, r"""
\unitssection

\section*{Sample screening levels}

\highlightbox{Some government agencies have developed standards and screening levels for
toxic chemicals in the air based on health information about the chemicals.
There is no information available for some toxic chemicals. The agencies are
listed below, with a brief description of the methods used in establishing their
levels. States may not be required to adhere to national standards.}

\begin{itemize}
"""
        for standard in self.standards():
            description = self.standards()[standard].description()
            if description is not None:
                print >>fh_null, '\item ' + md.convert(description)
            else:
                print >>fh_null, '\item ' + standard + ': description not available'


        print >>fh_null,"""
\end{itemize}


\end{document}
"""

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
        os.chdir(doc_dir)
        self._pdflatex_stat=os.system("pdflatex -interaction nonstopmode " + outfile.name + ">& /dev/null")
        doc_basename=os.path.splitext(outfile.name)[0]

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

    def _unit_representations(self):
        return {'ug/m3' :   '{\micro g/m\cubed}'}

    def _unit_descriptions(self):
        return {'ug/m3' : 'micrograms per cubic meter',
                'ppbv'  : 'parts per billion by volume',
                'ppb'   : 'parts per billion'}
    

