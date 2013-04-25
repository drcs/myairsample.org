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


