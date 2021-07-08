import json
import matplotlib.pyplot as plt

with open('hello_world_log.txt') as f:
    data = json.load(f)

phistories = {}
for key in data['spec']:
    if 'min' in data['spec'][key]: 
        phistories[key] = []

for pop in data['population_history']:
    for key in data['spec']:
        arr = [param[key] for param in pop['population']]
        
        if 'min' in data['spec'][key]: 
            vrange = data['spec'][key]['max'] - data['spec'][key]['min']
            phistories[key].append(((sum(arr) / len(arr)) - data['spec'][key]['min']) / (vrange if vrange != 0 else data['spec'][key]['min']))

for key in phistories:
    plt.plot(phistories[key])

plt.show()