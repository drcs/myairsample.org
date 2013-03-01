
from loc.report import LocReport
from loc.markdown_ltx import MarkdownLtx
from sys import stdout
import os
from tempfile import NamedTemporaryFile

md=MarkdownLtx()

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

        def ltx_def(name,value):
            print >>fh, '\\newcommand{\\' + name + r"} {" + value + "} \n"

        def ltx_def_if(name, value, default=None):
            if value is not None:
                ltx_def(name, value)
            elif default is not None:
                ltx_def(name, default)

        print >>fh,r"""
\documentclass{article}

\usepackage{fancyhdr, graphicx, pslatex, array}
\usepackage[table]{xcolor}

\raggedbottom
\widowpenalty=1000
\clubpenalty=1000

\newcommand{\stdfooter}{%
  \fancyhf{}
  \fancyhfoffset{0.2in}
  \fancyfoot[L]{
     \parbox{\logowidth}{
       \includegraphics[width=\logowidth]{labb_logo}\\
       \vskip 0.1in
       \includegraphics[width=\logowidth]{drcs_logo-200}
     }
     \setlength\acklength{\textwidth}
     \addtolength\acklength{-\logowidth}
     \addtolength\acklength{-0.5in}
     \hskip 0.5in
     \parbox{\acklength}{
       This report was generated at www.myairsample.org, a site developed and
       maintained by the Louisiana Bucket Brigade and Digitial Resources for
       Community and Science.  For questions and comments about air data,
       Louisiana Bucket Brigade can contacted at www.labucketbrigade.org,
       4226 Canal St, New Orleans, LA 70119, phone: 504-484-3433, fax:
       504-324-0332, email: info@labucketbrigade.org.
       For comments, feedback, or errors in the web site,
       please contact the LA Bucket Brigade or email Digital Resources for
       Community and Science at drcsdirector@gmail.com
     }
  }
}

\fancypagestyle{plain}{\stdfooter}
\pagestyle{empty}
% \pagestyle{fancy}
\stdfooter

\setlength{\parindent}{0pt}%
\setlength{\parskip}{\baselineskip}%
\setlength{\oddsidemargin}{0in}
\setlength{\textwidth}{6.5in}
\newlength\acklength
\newlength\logowidth
\setlength\logowidth{1.8in}
\addtolength\voffset{-0.5in}

\setlength{\arrayrulewidth}{1.5pt}

\newcommand{\cubed}{$^3$}
\newcommand{\micro}{$\mu$}
\newcommand{\fc}{\cellcolor{salmon}}
\newcommand{\nfc}{\cellcolor{white}}
\definecolor{salmon}{rgb}{1.0,0.8,0.7}
\newcommand{\highlightbox}[1]{\colorbox{salmon}{\parbox{\linewidth}{#1}}}
"""

        ltx_def('inunits',  self.units('in_rep'))
        ltx_def('outunits', self.units('out_rep'))
        ltx_def('longinunits',  self.units('in_long'))
        ltx_def('longoutunits', self.units('out_long'))

        ltx_def_if('samplename',     self.sample()['name'])
        ltx_def_if('sampledate',     self.sample()['date'])
        ltx_def_if('samplelocation', self.sample()['location'])

        user=""
        if self.user('first'):  user = 'For ' + self.user('first')
        if self.user('second'): user = user + r'\\ ' + self.user('second')
        ltx_def('user', user)

        print >>fh,r"""
\begin{document}

\title{Levels of Concern Report \\
       \large
       A comparison of air sampling results to pollutant levels of concern}
\author{\user}
\date{}
\maketitle

\section*{Sample information}
\begin{itemize}
\ifx\samplename\undefined\relax\else\item Sample identifying name:   \samplename\fi
\ifx\sampledate\undefined\relax\else\item Date sample was taken:     \sampledate\fi
\ifx\samplelocation\undefined\relax\else\item Location sample was taken: \samplelocation\fi
\item Report date:               \today
\item Report input units:        \longinunits\ (\inunits)$^*$
\item Report output units:       \longoutunits\ (\outunits)$^*$
\item Report made on web at:     http://myairsample.org
\end{itemize}

$^*$For a description of what units mean, see ``Units Information'' section later in this report

\newcommand{\unitssection}{
\section*{Units information}
Parts per billion (ppb) describes how many weighed parts of a chemical there
are for 1 billion parts of air. For example, a recipe says to add just a drop of
vanilla for every 100 pounds of flour. The drop of vanilla weighs hardly
anything, but it has a big effect on the cookies' flavor. Similarly, if we measure
benzene in the air, we might find 3 ``drops'' of benzene for 1,000,000,000
(one billion) ``drops'' of air. It seems like a small amount, but it is significant.

Parts per billion by volume, or ppbv, means the concentration has been figured
out in terms of how much space the molecules take up. For example, if we
make a mixture of 3 cups of vanilla and 1 billion cups of flour, then our
concentration is 3 parts volume (cups of vanilla) per billion parts volume (cups
of flour), or 3 ppbv sugar in flour. When 3 volumes of benzene are in a billion
volumes of air, the concentration is 3 ppbv benzene in air.

Micrograms per meters cubed (\micro g/m\cubed) describes how much of a chemical's
weight is in a volume of air that takes up one cubic meter. Imagine an empty
box that is three feet long on both sides, and three feet tall. One meter is about
three feet long. So the box's volume is 1 cubic meter, or 1 m\cubed. A microgram
(\micro g) is a very small weight, like that of a grain of sand. You put 3 grains of sand
into the box. The concentration of sand inside the box is the weight of the sand
(3 \micro g) divided by the
volume of the box (1 m\cubed), or 3 \micro g /m\cubed. Like grains of sand, chemicals can also be
reported by weight and volume. For example, a monitor might read 5 \micro g /m\cubed\ %
benzene, or 5 \micro g of benzene in 1 m\cubed\ of air.
}
"""
        self._results_section(fh)

        # Standards descriptions
        print >>fh, r"""
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
                print >>fh, '\item ' + md.convert(description)
            else:
                print >>fh, '\item ' + standard + ': description not available'


        print >>fh,"""
\end{itemize}


\end{document}
"""

    def generate(self):
        image_dir = os.path.join(os.getcwd(), 'media')
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
            return ["Content-type: text/plain"]
        else:
            return ["Content-type: application/pdf",
                    "Content-disposition: attachment; filename=LABB-%s.pdf" % username]

    def _unit_representations(self):
        return {'ug/m3' :   '{\micro g/m\cubed}'}

    def _unit_descriptions(self):
        return {'ug/m3' : 'micrograms per cubic meter',
                'ppbv'  : 'parts per billion by volume',
                'ppb'   : 'parts per billion'}
    

