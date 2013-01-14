
from loc.report import LocReport
from loc.markdown_ltx import MarkdownLtx
from sys import stdout
import os
from tempfile import NamedTemporaryFile


# Markdown converter for use globally
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

class LabbReport(LocReport):

    def generate_tex(self, fh=stdout):

        def ltx_tr(xs):
            return str.join(' & ',map(str,xs)) + r'\\'

        def ltx_def(name,value):
            print >>fh, '\\newcommand{\\' + name + r"} {" + value + "} \n"

        def ltx_def_if(name, value, default=None):
            if value is not None:
                ltx_def(name, value)
            elif default is not None:
                ltx_def(name, default)

        print >>fh,r"""
\documentclass{article}

\usepackage{fancyhdr, graphicx, pslatex}
\usepackage[table]{xcolor}

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
       504-324-0332.  For comments, feedback, or errors in the web site,
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

\newcommand{\cubed}{$^3$}
\newcommand{\micro}{$\mu$}
\newcommand{\fc}{\cellcolor{red}}
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

        user="N/A"
        if self.user('first'):  user = self.user('first')
        if self.user('second'): user = user + r'\\ ' + self.user('second')
        ltx_def('user', user)

        print >>fh,r"""
\begin{document}

\title{Levels of Concern Report}
\author{For \user}
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

$^*$For a description of what units mean, see ``Unit Information'' section later in this report

\newcommand{\unitssection}{
\section*{Unit information}
Parts per billion (ppb) describes how many weighed parts of a chemical there
are for 1 billion parts of air. For example, a recipe says to add a just a drop of
vanilla for every 100 pounds of flour. The drop of vanilla weighs hardly
anything, but it has a big effect on the cookies' flavor. Similarly, if we measure
benzene in the air, we might find 3 ``drops'' of benzene for 1,000,000,000
(billion) ``drops'' of air. It seems like a small amount, but it is significant.

Parts per billion by volume, or ppbv, means the concentration has been figured
out in terms of how much space the molecules take up. For example, if we
make a mixture of 3 cups of vanilla and 1 billion cups of flour, then our
concentration is 3 parts volume (cups of vanilla) per billion parts volume (cups
of flour), or 3ppbv sugar in flour. When 3 volumes of benzene are in a billion
volumes of air, the concentration is 3ppbv benzene in air.

Micrograms per meters cubed (\micro g/m\cubed) describes how much of a chemical's
weight is in a volume of air that takes up one cubic meter. Imagine an empty
box that is three feet long on both sides, and three feet tall. One meter is about
three feet long. So the box's volume is 1 cubic meter, or 1 m 3. A microgram
(\micro g) is a very small weight, like that of a grain of sand. You put 3 grains of sand
into the box. The concentration of sand inside the box is 3 \micro g divided by the
volume of the box 1 m3, or 3 \micro g /m3. Like grains of sand, chemicals can also be
reported by weight and volume. For example, a monitor might read 5 \micro g /m\cubed
benzene, or 5 \micro g of benzene in 1 m\cubed of air.
}

\newpage
\section*{Sample Analysis}

% \highlightbox{The information below is provided to guide discussion on how
% exposure to chemicals can affect you, your family, and your
% community. This information is paraphrased from the ATSDR ``ToxFAQs''
% website available at http://www.atsdr.cdc.gov/substances/index.asp.}
"""
        for chemical in self.chemicals():
            # chemical.keys() == 'name','level','level_rep',
            #                    'mw','cas','comparisons'
            print >>fh,r'\subsection*{' + chemical['name'] + r"""}

% Chemical description would go here when implemented

\begin{tabular}{|c|c|p{3in}|}
\hline
The level in your bucket sample &                             & Comparison Level                                       \\
\hline
"""
            for comparison in chemical['comparisons']:
                # comparison.keys=='source','level_rep','level',
                #                  'criterion','description'
                # comparison['criterion']['description']['brief']
                if chemical['level'] > comparison['level']:
                    fc=r' \fc '
                else:
                    fc = ''
                print >>fh, ltx_tr([
                        fc + chemical['level_rep'] + '\ \outunits',
                        fc + md.convert(comparison['description']),
                        fc + md.convert(comparison['criterion']['description']['brief']) + ' ' + comparison['level_rep'] + '\ \outunits'
                        ])
                print >>fh, r'\hline '

            print >>fh, r"""
\hline
\end{tabular}
"""

        for name in self.failed_lookups():
            print >>fh, r'\subsection*{' + name + r"""}
\begin{tabular}{|c|c|p{3in}|}
\hline
The level in your bucket sample &                             & Comparison Level                                       \\
\hline
"""

            print >>fh, ltx_tr([
                    chemical['level_rep'] + '\ \outunits',
                    "",
                    r'Either a comparison level is not available for ' + name + ' or the spelling of the chemical name is incorrect.'
            ])
            print >>fh, r"""
\hline
\end{tabular}
"""

        for name in self.failed_conversions():
            print >>fh, r'\subsection*{' + name + r"""}

Unit conversions failed.  (Try ppb or ug/m3?)
"""

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
        result=os.system("pdflatex " + outfile.name + ">& /dev/null")
        doc_basename=os.path.splitext(outfile.name)[0]

        os.system("cat " + doc_basename + ".pdf")
        stdout.flush()
            
        cleanup(doc_basename + '.log')
        cleanup(doc_basename + '.aux')
        cleanup(doc_basename + '.pdf')

    def http_headers(self):
        username = self.user('first') + '_' + self.user('second')
        return ["Content-type: application/pdf",
                "Content-disposition: attachment; filename=LABB-%s.pdf" % username]

    def _unit_representations(self):
        return {'ug/m3' :   '{\micro g/m\cubed}'}

    def _unit_descriptions(self):
        return {'ug/m3' : 'micrograms per cubic meter',
                'ppbv'  : 'parts per billion by volume',
                'ppb'   : 'parts per billion'}
    

