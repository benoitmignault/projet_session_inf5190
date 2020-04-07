export FLASK_APP=index.py
export FLASK_ENV=development


run:
	raml2html doc.raml > templates/doc.html
	flask run
