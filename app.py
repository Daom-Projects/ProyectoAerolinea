import os
from datetime import datetime
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    dato = request.form.get('dato')
    if dato:
        import urllib.request
        import json
        import os
        import ssl

        def allowSelfSignedHttps(allowed):
            # bypass the server certificate verification on client side
            if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                ssl._create_default_https_context = ssl._create_unverified_context

        allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
        data =  {
            "Inputs": {
                "WebServiceInput0": [
                    {
                        "avail_seat_km_per_week": dato
                    }
                ]
            },
            "GlobalParameters": {}
        }

        body = str.encode(json.dumps(data))

        url = 'http://7eb27ebc-6c15-4ade-b1bb-838f85815911.eastus.azurecontainer.io/score'
        api_key = 'Uv7e2e4hK63eEkOeCx6cVZNBPdFONBHV' # Replace this with the API key for the web service

        # The azureml-model-deployment header will force the request to go to a specific deployment.
        # Remove this header to have the request observe the endpoint traffic rules
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            print(result)
            prediccion = result[-22:-4].decode("utf-8")
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))
        return render_template('hello.html', prediccion = prediccion, entrada = dato)
    else:
        flash('El valor no ha llegado o es invalido','error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()