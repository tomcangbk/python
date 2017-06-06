# Get size of file
def get_file_size(path_of_file):
  return os.path.getsize(path_of_file)

# Change file to list
def file_to_list(file_name):
	results = []
	f = open(file_name)
	for line in f:
		results.append(line.rstrip())
	random.shuffle(results)
	return results
    
# Write list to file
def list_to_file(file_name, thelist):
	f = open(file_name, "w")
	for item in thelist:
		f.write("%s\n" % item)

# Delete file content
def deleteContent(file_name):
	with open(file_name, "w"):
		pass

# Download video from youtube
def download(link):
	command = "C:/Python27/Scripts/pytube.exe -e mp4 -f "" -r 720p -p C:/VidMaker/tmp "+ link
	subprocess.check_call(command, shell = False)

# Show MAC address
def getMacAddress():  
	for line in os.popen("ipconfig /all"): 
		if line.lstrip().startswith('Physical Address'): 
			mac = line.split(':')[1].strip().replace('-',':') 
			break 
	return mac
  
 
