import json
import sys
import os

file = sys.argv[1]

countries = {}
_id = None
with open(file) as handle:

    current = {}
    for line in handle:
        line = line.rstrip()

        if '!ID' in line:
            if _id:
                countries[_id] = current
            _id = int(line.replace('!ID', '').strip())
            current = {}

        if '!v' in line:
            line = line.split("!")
            v = int(line[1].replace('v', ''))
            content = line[2]

            current[v] = content
countries[_id] = current

output = []
for pk, country in countries.items():

    current = {}
    current['pk'] = pk
    current['model'] = 'main.country'
    current['fields'] = {
        'code': country[102].upper(),
        'name': country[30],
    }

    output.append(current)

lang_id = 1
for pk, country in countries.items():

    if 20 in country.keys():
        current = {}
        current['pk'] = lang_id
        current['model'] = 'main.countrylocal'
        current['fields'] = {
            'country': pk,
            'name': country[20],
            'language': 'pt-br',
        }

        output.append(current)
        lang_id += 1

for pk, country in countries.items():

    if 40 in country.keys():
        current = {}
        current['pk'] = lang_id
        current['model'] = 'main.countrylocal'
        current['fields'] = {
            'country': pk,
            'name': country[40],
            'language': 'es',
        }

        output.append(current)
        lang_id += 1

print json.dumps(output, indent=2)
