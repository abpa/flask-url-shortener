from flask import Flask, request, redirect, abort, jsonify
from flask_cors import CORS, cross_origin

import uuid

app = Flask(__name__)
app.config['BASE_URL'] = '127.0.0.1:5000'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)

hash_table = {}

def get_random_key():
	return uuid.uuid4()

def get_unique_keys():
	short_url = None
	found = True
	while(found):
		short_url = get_random_key()
		try:
			val = hash_table[short_url]
		except Exception as e:
			found = False
	return short_url

@app.route('/shorten', methods=['POST', 'OPTIONS'])
@cross_origin()
def shorten():
	if request.method == "OPTIONS":
		return _build_cors_prelight_response()
	error = []
	short_url = None
	url = None
	
	if request.method == "POST":
		content = request.json
		try:
			print(content)
			url = content['url']
			short_url = get_unique_keys()
			hash_table[short_url] = url
		except Exception as e:
			print(e)
			error.append("Unable to get URL. Please make sure it's valid and try again.")
	print(error)
	return _corsify_actual_response(jsonify({
		'original': url,
		'result': app.config['BASE_URL']+'/'+str(short_url),
		'error': error
		}))

@app.route('/all', methods=['GET'])
def all_hashes():
	result = []
	keys = hash_table.keys()
	for key in keys:
		result.append({
			'val': app.config['BASE_URL'] + '/' + str(key),
			'url': hash_table[key]
		})
	return {'count': len(result), 'result': result}


@app.route('/<hash>', methods=['GET'])
@cross_origin()
def resolve(hash):
	try:
		val = hash_table[float(hash)]
		return redirect(val, code=302)
	except Exception as e:
		print(e)
	abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return "Aborted with 404", 404

# https://stackoverflow.com/a/52875875
def _build_cors_prelight_response():
    response = make_response()
	# TODO * to be specific url
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    return response


if __name__ =="__main__":
	app.run(debug = True)