def mangle(s):
    return s.strip()[1:-1]

def cat_json(output_filename, input_filenames):
    with open(output_filename, "w") as outfile:
        first = True
        for infile_name in input_filenames:
            with open(infile_name) as infile:
                if first:
                    outfile.write('[')
                    first = False
                else:
                    outfile.write(',')
                outfile.write(mangle(infile.read()))
        outfile.write(']')
outputfilename='output.json'
input_filenames=[]
for i in range(2,2182):
    input_filenames.append('da'+str(i)+'.json')
print(input_filenames)
cat_json(outputfilename,input_filenames)
