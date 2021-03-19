import json

from collections import OrderedDict

print("loading manifest...")
manifest = json.load(open('manifest.json'))
print(manifest)

print("importing...")
module = __import__(manifest['info']['main'])

print("module.main(manifest)")
module.main(manifest)

