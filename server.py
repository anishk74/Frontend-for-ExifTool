import sys
import subprocess
from flask import Flask, render_template, request, Markup

def get(filename,pathET):
	return subprocess.run([pathET,'-h',filename], stdout=subprocess.PIPE).stdout.decode('utf8')

def update(filename, longitude, latitude,pathET):
	temp=subprocess.run([pathET,
					'-XMP:GPSLongitude=\"'+str(longitude)+'\"',
					'-XMP:GPSLatitude=\"'+str(latitude)+'\"', filename])
	return get(filename,app.config.get('path_to_exiftool'))

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
	return render_template('index.html')

@app.route('/metadata/', methods=["GET","POST"])
def getMetaData():
	fileform=request.form
	f=request.form.get("filename")
	#print(f)
	meta = "File not Found"
	if f!=None:
		meta = get(f,app.config.get('path_to_exiftool'))
	return render_template('metadata.html',text=meta,form=fileform)
	
@app.route('/addedgps/', methods=["GET","POST"])
def addedgps():
	imgname=request.form.get("filename")

	gpsform=request.form
	f=request.form.get("filename")
	longitude=gpsform.get("long")
	latitude=gpsform.get("lat")
	print(type(latitude))
	#print(longitude,latitude,f)
	meta=update(f,longitude,latitude,app.config.get('path_to_exiftool'))
	#print(type(gpsform.items()))
	return render_template("metadata.html",text=meta,form=gpsform)



if __name__ == '__main__':
	
	print(sys.argv)
	app.config['path_to_exiftool'] = sys.argv[1]
	app.run(debug=True)
