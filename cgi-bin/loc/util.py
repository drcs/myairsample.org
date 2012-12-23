def canonical_name(s):
    try: return s.lower().strip()
    except AttributeError: return s

