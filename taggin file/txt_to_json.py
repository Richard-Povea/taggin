import json


with open("1039.json") as file:
    final_data = list()
    for index, line in enumerate(file):
        line = line.split(' ')
        
        data = {"path": line[0], 
                "file": line[0].split('/')[-1],
                "beginning": float(line[1]), 
                "end": float(line[2]),
                "taxonomy": line[3][:-1]}

        final_data.append(data)
    json_object = json.dumps(final_data, indent = 4)
    with open("1039_modificado_v2.json", "w") as outfile:
        outfile.write(json_object)
        