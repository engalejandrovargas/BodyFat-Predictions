from flask import Flask, request, render_template, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField

import pickle

file1 = open('bodyfatmodel1.pkl', 'rb')
rf = pickle.load(file1)
# file1.close()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


class InfoForm(FlaskForm):

    density = DecimalField('density')
    abdomen = DecimalField('abdomen')
    chest = DecimalField('chest')
    weight = DecimalField('weight')
    hip = DecimalField('hip')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def predict():
    string = False
    form = InfoForm()
    if form.validate_on_submit():
        
        density = form.density.data
        abdomen = form.abdomen.data
        chest = form.chest.data
        weight = form.weight.data
        hip = form.hip.data

        input_features = [[density, abdomen, chest, weight, hip]]
        prediction = rf.predict(input_features)[0].round(2)

        string = 'Percentage of Body Fat Estimated is : ' + str(prediction)+'%'
        flash(string)
        return render_template('home.html', form=form, string=string)

    return render_template('home.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
