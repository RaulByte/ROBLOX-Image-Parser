# RaulByte/Lance Feb 22 2019

import urllib.request  # Yes
import flask  # Yes
from flask import request, jsonify, send_file  # Yes
import requests  # Yes
from PIL import Image # Yes
import os
import sys
import io  # Yes

app = flask.Flask(__name__)
app.config['DEBUG'] = True

# HOME PAGE
@app.route('/', methods=["GET"])
def home():
	return flask.render_template('home.html')


def checkImgExistsAndFetchType(imgName):
	# Check Online
	image_formats = ('image/png', 'image/jpeg', 'image/jpg', 'image/webp')
	r = requests.head(imgName)
	if r.headers["content-type"] in image_formats:
		return "online"

	return False

@app.route('/api/archive/img', methods=['GET'])
def api_pullArchive():

	if 'show' in request.args:
		image_type = checkImgExistsAndFetchType(request.args['show'])
		if image_type == 'online':
			return '<img src={}>'.format(request.args['show'])
		return "File Unavailable" #flask.render_template('arg_error.html')

	if 'pull' in request.args:
		pixel_array = ""
		if checkImgExistsAndFetchType(request.args['pull']) != False:
			print("Starting Write")
			url_data = urllib.request.urlopen(request.args['pull'])
			open_image = Image.open(io.BytesIO(url_data.read()))
			open_image = open_image.resize((400,400), Image.BILINEAR)
			rgb_image = open_image.convert('RGB')
			#pixel_array.append((open_image.size))
			pixel_array += '[{},{}]'.format(open_image.size[0], open_image.size[1])
			for xRange in range(open_image.size[0]):
				for yRange in range(open_image.size[1]):
					r = rgb_image.getpixel((xRange, yRange))[0]
					g = rgb_image.getpixel((xRange, yRange))[1]
					b = rgb_image.getpixel((xRange, yRange))[2]
					#pixel_array.append("{},{},{}".format(r,g,b))
					pixel_array += "/{},{},{}/".format(r,g,b)
			print("Converted")
			print(pixel_array)

			return jsonify(pixel_array)

	return flask.render_template('archive.html')

app.run()
