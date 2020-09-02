import json

print("loading manifest...")
manifest = json.load(open('manifest.json'))
print(manifest)

print("importing...")
m = __import__(manifest['main'])

print("m.main(manifest)")
m.main(manifest)

