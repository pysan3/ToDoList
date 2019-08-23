import apps.app as backapp

print(backapp.load_file(1))
print(dict({'valid': '1'}, **backapp.load_file(1)))