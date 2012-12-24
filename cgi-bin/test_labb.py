
from loc.labb_report import LabbReport

report1 = LabbReport(chemicals=[{'name':  'benzene',           'level': '0.1442'},
                                {'name':  'toluene',           'level': '43.3252'},
                                {'name':  'frop',              'level': '1.11'},
                                {'name':  'vinyl chloride',    'level': '4322.3252'},
                                {'name':  'trichloroethylene', 'level': '1143.3252'}
                                ])

report1.generate()
