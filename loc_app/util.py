from math import log10

def canonical_name(s):
    try: return s.lower().strip()
    except AttributeError: return s
    
def _first_decile_comparison_description(compare):
    factor  = int(compare + 0.25)
    decimal = (compare + 0.25) - factor
    factor_str = {
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine'
    }[factor]

    if   (decimal < 0.5):  return factor_str + ' times'
    return                        factor_str + '-and-a-half times'

def describe_comparison(level,reference):
    """Describe the comparison between a level and a reference as an integer ratio,
       and one of Gwen's descriptive words"""
    compare = level / reference

    if compare > 10:       return "is " + int(round(compare)) + " times"
    if compare > 1.25:     return "is " + _first_decile_comparison_description(compare)
    if compare > 1.0:      return "exceeds"
    
    return "is below"
        
def convert_units(level, from_units, to_units, mw=None):
    mw_air = 28.9666      # g mol-1
    R      = 8.2057e-5    # m^3 atm K-1 mol-1
    T      = 298          # K ; standard ambient temperature
    P      = 0.986        # atm; standard pressure
    factor = { 'ppm'         : 1.0 ,
               'ppb'         : 1000.0 ,
               'ug/m3'       : mw_air * P / (R * T) ,
               'mg/m3'       : 1000 * mw_air * P / (R * T) ,
    }
    if ((from_units == 'ppbv') or (to_units == 'ppbv')):
        factor['ppbv'] = mw_air * 1000 / mw
    return level / factor[from_units] * factor[to_units]

def fmt_sigfigs(x,n=3):
    digits = int(log10(x))
    fmt = '%d'
    if (digits < n):
        fmt = '%%.%df' % (n - digits)
    return fmt % x


