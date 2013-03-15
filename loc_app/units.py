
units = {
    'ppb'  : {'description' : 'parts per billion'},
    'ppbv' : {'description' : 'parts per billion by volume'},
    'ug/m3': { 'description': 'micrograms per cubic meter',
               'representation': '&micro;g/m^3^'}
}

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


