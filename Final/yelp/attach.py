import json

for i in range(2,2182):
    x='data'+str(i)+'.json'
    y='da'+str(i)+'.json'
    with open(x, "r") as f:
        elevation=json.load(f)
    with open(y,"w") as f:
        json.dump(elevation['businesses'],f)
