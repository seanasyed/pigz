import os 
import shutil
import wget 
import tarfile
import time
import gzip

DATA_PATH = "data"
dataURL = "http://corpus.canterbury.ac.nz/resources/large.tar.gz"

# Download dataset
try:
	os.mkdir("data")
except: 
	pass
	
print("Retrieving dataset from {}...".format(dataURL))
wget.download(dataURL, out=os.path.join(DATA_PATH, "large.tar.gz"))

# Decompress dataset
tar = tarfile.open(os.path.join(DATA_PATH, "large.tar.gz"))
tar.extractall(path=DATA_PATH)
tar.close()
os.remove(os.path.join(DATA_PATH, "large.tar.gz"))

# Compile compression executables
# gzip already compied
# pigz & zopfli
os.system("make")

''' 
For each algo, we need to collect the following info: 

- Compression time
- Compression ratio
'''

# Gzip benchmarking

# Compression time
gzipTime = time.time()

for filename in os.listdir(DATA_PATH): 
	with open(os.path.join(DATA_PATH, filename), 'rb') as f_in: 
		with gzip.open(os.path.join(DATA_PATH, filename + ".gz"), 'wb') as f_out: 
			shutil.copyfileobj(f_in, f_out)

gzipTime = time.time() - gzipTime
print("gzip compression took {}s".format(gzipTime))

for filename in os.listdir(DATA_PATH): 
	if filename.endswith(".gz"):
		os.remove(os.path.join(DATA_PATH, filename))

# TODO Benchmark zopfli

#Compression time
zopfliTime = time.time()

for filename in os.listdir(DATA_PATH): 
	os.system("./pigz -11 {}".format(os.path.join(DATA_PATH, filename)))

zopfliTime = time.time() - zopfliTime
print("zopfli compression took {}s".format(zopfliTime))

for filename in os.listdir(DATA_PATH): 
	if filename.endswith(".gz"):
		os.remove(os.path.join(DATA_PATH, filename))

# Benchmark pigz

# Compression time
pigzTime = time.time()
for filename in os.listdir(DATA_PATH): 
	os.system("./pigz {}".format(os.path.join(DATA_PATH, filename)))

pigzTime = time.time() - pigzTime
print("pigz compression took {}s".format(pigzTime))

for filename in os.listdir(DATA_PATH): 
	if filename.endswith(".gz"):
		os.remove(os.path.join(DATA_PATH, filename))

# Delete dataset
shutil.rmtree(DATA_PATH)
print("Dataset removed from device")

# Clean working directory
os.system("make clean")
print("Working directory clean")