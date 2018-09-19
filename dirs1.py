import os

chart_count = 0
os.chdir('/root/vector')

def parse_chart(file_name):
	global chart_count
	print file_name
	chart_count+=1

dirs = os.listdir('.')

for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    #print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        #print(len(path) * '---', file)
	filename, file_extension = os.path.splitext(file)
	print filename, file_extension
	if file_extension == '.000':
		parse_chart(file)

print chart_count
