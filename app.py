from traceback import print_tb
from flask import Flask, render_template,request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import os


app=Flask(__name__)  # Intialize Flask app

@app.route('/', methods=['GET'])  #Route to Display home page   
@cross_origin()
def homePage():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST']) #Route to show predicted results page
@cross_origin()
def price_predict():
    if request.method == 'POST':

        crim=float(request.form['CRIM'])  
        zn=float(request.form['ZN'])
        indus=float(request.form['INDUS'])
        chas=float(request.form['CHAS'])
        nox=float(request.form['NOX'])
        rm=float(request.form['RM']) 
        age=float(request.form['AGE'])
        dis=float(request.form['DIS'])
        rad=float(request.form['RAD'])
        ptratio=float(request.form['PTRATIO'])
        b=float(request.form['B'])
        lstat=float(request.form['LSTAT'])

        model_filename='finalized_model.pickle'
        currentpath=os.getcwd()
        final_model_filepath=os.path.join(currentpath, model_filename)

        scaler_file="scaler.pkl"
        #final_scaler_filepath=os.path.join(currentpath,scaler_file)

            

        feaures_nonscale=[crim,zn,indus,chas,nox,rm, age,dis,rad,ptratio,b,lstat]
                
                
        #scaler_model=pickle.load(open(final_scaler_filepath, 'rb'))
        scaler_model=pickle.load(open(scaler_file, 'rb'))
        features_scaled=scaler_model.transform([feaures_nonscale])
        # scaler_model.inverse_transform()

        
        load_housing_model=pickle.load(open(final_model_filepath,'rb')) # loading the model file from the storage
        # predictions using the loaded model file

        #prediction=load_housing_model.predict([[crim,zn,indus,chas,nox,rm,age,dis,rad,ptratio,b,lsat]])

        prediction=load_housing_model.predict(features_scaled)
        print(prediction)
        return render_template('results.html',prediction=prediction[0])
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app