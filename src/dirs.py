import os

chart_count = 0
os.chdir('/root/vector')

def parse_chart(file_name):
	print file_name
	chart_count+=1

dirs = os.listdir('.')

for dir in dirs:
  	if os.path.isdir(dir):
        	print("directory: %s" % dir)
		os.chdir(dir)
    		subdirs = os.listdir(".")
    		for subdir in subdirs:
			if os.path.isdir(subdir):
				print("error: nested dir %s" % subdir)
			else:
				filename, file_extension = os.path.splitext(subdir)
				if file_extension == '000':
					parse_chart(subdir)
		os.chdir('..')
	else:
		parse_chart(dir)
