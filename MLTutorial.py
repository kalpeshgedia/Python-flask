import urllib3, requests, json, os
from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import Required, Length, NumberRange


url = 'https://us-south.ml.cloud.ibm.com'
username = '**********'
password = '**********'
scoring_endpoint = '*****************'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretpassw0rd'
#bootstrap = Bootstrap(app)
class ReusableForm(Form):
  NPG = TextField('NPG:', validators=[validators.required()])
  PGL = TextField('PGL:', validators=[validators.required()])
  DIA = TextField('DIA:', validators=[validators.required()])
  TSF = TextField('TSF:', validators=[validators.required()])
  INS = TextField('INS:', validators=[validators.required()])
  BMI = TextField('BMI:', validators=[validators.required()])
  DPF = TextField('DPF:', validators=[validators.required()])
  Age = TextField('Age:', validators=[validators.required()])
@app.route('/', methods=['GET', 'POST'])
def index():
  form = ReusableForm()
  if request.method == 'POST':
    NPG=int(request.form['NPG'])  
    PGL=int(request.form['PGL'])
    DIA=int(request.form['DIA'])  
    TSF=int(request.form['TSF'])  
    INS=int(request.form['INS'])
    BMI=float(request.form['BMI'])  
    DPF=float(request.form['DPF']  )
    Age=int(request.form['Age'])
    headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
    path = '{}/v3/identity/token'.format(url)
    response = requests.get(path, headers=headers)
    mltoken = json.loads(response.text).get('token')
    scoring_header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    #payload = {"fields": ["NPG", "PGL", "DIA", "TSF", "INS", "BMI", "DPF", "AGE"], "values": [[6,148,72,35,0,33.6,0.627,50]]}
    payload = {"fields": ["NPG", "PGL", "DIA", "TSF", "INS", "BMI", "DPF", "AGE"], "values": [[NPG,PGL,DIA,TSF,INS,BMI,DPF,Age]]}
    scoring = requests.post(scoring_endpoint, json=payload, headers=scoring_header)
    scoring_json = scoring.json()
    fields = scoring_json["fields"]
    values = scoring_json["values"]
    single_value = values[0]
    print(single_value)
    probability_index = fields.index("probability")
    prediction_index = fields.index("prediction")
    rawPrediction_index = fields.index("rawPrediction")
    refined_score = {
      "probability": single_value[probability_index],
      "prediction": single_value[prediction_index],
      "rawPrediction": single_value[rawPrediction_index]
    }
      
    flash(single_value)
    
    return render_template('score.html', form=form, scoring=refined_score)
  return render_template('index-1.html', form=form)
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
  app.run()
