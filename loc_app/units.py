
units = {
    'ppb'  : { 'description' : 'parts per billion',           'sort' : 3,
               'representation': 'ppbm' },
    'ppbv' : { 'description' : 'parts per billion by volume', 'sort' : 2},
    'ug/m3': { 'description' : 'micrograms per cubic meter',  'sort' : 1,
               'representation': '&micro;g/m^3^'}
}

def unit_keys():
    return sorted(units.keys(), key=lambda k: units[k]['sort'])

# 'md' is a Markdown instance implementing a 'conert' method
def represent(key):
    """Return a markdown representation of units named by 'key',
    if available
    """
    if key in units and 'representation' in units[key]:
        return units[key]['representation']
    else:
        return key

def describe(key):
    if key in units and 'description' in units[key]:
        return units[key]['description']
    else:
        return key


