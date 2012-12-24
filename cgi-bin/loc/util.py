from math import log10

def canonical_name(s):
    try: return s.lower().strip()
    except AttributeError: return s

def describe_comparison(level,reference):
    """Describe the comparison between a level and a reference as an integer ratio,
       and one of Gwen's descriptive words"""
    compare = level / reference
    decimal = compare - int(compare)
    factor  = int(compare)
    description = 'unknown'
    if   (compare <= 1.0): return "is below"
    elif (compare < 1.8):  return "exceeds"
    elif (decimal < 0.2):  return "is about " + str(factor) + " times"
    elif (decimal < 0.8):  return "is _over_ " + str(factor) + " times"
    else:                  return "is _nearly_ " + str(factor + 1) + " times"
        
def convert_units(level, from_units, to_units, mw=None):
    factor = { 'ppm'         : 1.0 ,
               'ppb'         : 1000.0 ,
               'ug/m3'       : 1198.0 ,
               'mg/m3'       : 1.198 }
    if ((from_units == 'ppbv') or (to_units == 'ppbv')):
        factor['ppbv'] = 24040.0 / mw
    return level / factor[from_units] * factor[to_units]

def represent_units(name):
    """Given a key 'name', return a markdown representation of how that
       unit should be represented in the output
    """
    # FIXME how to represent ug/m3 in markdown??
    unit_representations = {'ug/m3' :   '{\micro g/m\cubed}'}
    if name in unit_representations:
        return (unit_representations[name])
    else:
        return (name)

def fmt_sigfigs(x,n=3):
    digits = int(log10(x))
    fmt = '%d'
    if (digits < n):
        fmt = '%%.%df' % (n - digits)
    return fmt % x


