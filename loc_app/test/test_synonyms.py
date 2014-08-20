from loc.synonyms import name2cas,cas2mw

name='benzene'
cas=name2cas(name)
mw=cas2mw(cas)

print("name: %s"%name)
print("cas: %s"%cas)
print("mw: %f"%mw)


