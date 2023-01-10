from flask import Flask,request,render_template
import numpy as np
import pickle
import datetime
import pandas as pd 
from draw_graph import draw_graphs

data = pd.read_excel("Names.xlsx")

App_Officers = ['Rowney Cortin', 'Karol Ferre', 'Adelbert Heindrich',
       'Wilone Kaufman', 'Jasper Raccio', 'Krista Helin', 'Leoline Emlin',
       "Laure O'Sharry", 'Parry Shiel', 'Rafael Penchen', 'Jolene Hamby',
       'Eleanora Pattlel', 'Morry MacGibbon', 'Sauveur Da Costa',
       "Donni O'Shiel", 'Matthiew Tolley', 'Genny Doherty', 'Amos Brusby',
       'Shanda Chaston', 'Clarita Alldred', 'Malissa Wenderoth',
       'Shandra McChruiter', 'Brigit Pickle', 'Jemima Girdler',
       'Sophronia Gennrich', 'Tabbi Rounsefull', 'Misha Brendel',
       'Doralyn Jimeno', 'Lucian Tettley', 'Analise Gamon',
       'Pandora Couper', 'Pavlov McNirlan', 'Shaine Bate', 'Parry Puig',
       'Chadwick Demelt', 'Thatch Basterfield', 'Tonnie Kesteven',
       'Mattie Speeding', 'Bowie Magenny', 'Lyn Arenson', 'Kerry Plet',
       'Ethelyn Charrington', 'Lenora Titmuss', 'Etan Messent',
       'Stormie Deery']

Req_Officers = ['Bunny Spraggs', "Lorrayne O' Lone", 'Nicolette Convery',
       'Reuben Chiommienti', 'Ely Gwinnel', 'Ofilia Borrington',
       'Batsheva Danslow', 'Lesly Hallifax', 'Rebekah Jermy',
       'Silvie Whittock', 'Jocelin Figg', 'Tris Lerer',
       'Torey Falconer-Taylor', 'Kiah Friday', 'Bradney Legon',
       'Carline Ezzy', 'Marget Metts', 'Yorke Schuricke',
       'Tootsie Ganing', 'Lars Laraway', 'Dorothee Cahey',
       'Marshall Fanshawe', 'Torry Vamplus', 'Sofia Plumbe',
       'Joey Gallehock', 'Benita Maker', 'Perry Pieter',
       'Hannah Shildrick', 'Beryle Menicomb', 'Lloyd Cavaney',
       'Llewellyn Iacovacci', 'Anthiathia Treen', 'Susannah Sangar',
       'Jayme Birth', 'Gloriana Vaz']
Suppliers = ['Rosenbaum Group', 'Botsford, Rolfson and Pouros', 'Ferry-Dibbert',
       'Gusikowski Group', 'Hartmann Inc', 'Friesen-Ullrich',
       'Ward-Wolff', 'Swift-Friesen', 'Cummerata, Gibson and Herman',
       'Howell, Haley and Cremin', 'Bogan-Gerhold', 'Rosenbaum-Jones',
       'Kirlin, Kutch and Tremblay', 'Hessel-Bergnaum',
       'Ruecker, Senger and Feeney', 'Pouros-Mitchell', 'Witting Group',
       'Tillman-Larson', 'Monahan-Rippin', 'Miller-Lueilwitz',
       'Denesik LLC', 'Ryan, Turner and Schulist', 'Rohan-Runolfsdottir',
       'Hagenes, Kilback and Conroy', 'Koepp, Zulauf and Bins',
       'Krajcik, Fritsch and Ebert', 'Smith, Cummings and Auer',
       'Wuckert-Effertz', 'Schmitt-Kling', 'Rutherford, Murphy and Jast',
       'Rogahn and Sons', 'Jacobs, Senger and Dickens',
       'Ratke-Morissette', 'Sipes Inc', 'Bartell, Swaniawski and Kuhlman',
       'Kuvalis-Schiller', 'Spinka-Price', 'Hills-Rau', 'Hammes Inc',
       'Ward, Wisoky and Kiehn', 'Bartell, Lemke and MacGyver',
       'Shanahan, Watsica and Mayert', 'Schuster, Huels and Rolfson',
       'Herman and Sons', 'Paucek and Sons', 'Sanford LLC',
       'Koelpin-Brown', 'Nolan, Bahringer and Torphy', 'Leffler Inc',
       'Bayer, Haley and Hermann', 'Lebsack, Herzog and Mraz',
       "Maggio, O'Kon and McClure", 'Sipes-Schroeder', 'Bauch Inc',
       'Wilkinson Inc', 'Klein, Kilback and Wisozk',
       'Dare, Barrows and Gottlieb', 'Metz LLC', 'Waters and Sons',
       'Lind Group', 'Reynolds, Dooley and Doyle', 'Walsh Group',
       'Franecki-Kulas', 'Ward, Larkin and Swift',
       'Graham, Little and Kris', 'Vandervort, Nader and Reichert',
       'Thompson-Lowe', 'Cassin-Langosh', 'Murazik, Conn and Rodriguez',
       'Cummings-Gleason', 'Denesik Group', 'Marvin, Legros and Hoppe',
       'Gutkowski-Lynch', 'Toy-Ferry', 'Wehner-Stehr', 'Schiller-Cremin',
       'Kunze, Von and Leannon', 'Mante Inc', 'Lockman-Torphy',
       'Legros-Jacobs', 'Stanton-West', 'Maggio, Hahn and Jones',
       'Wolff, Wisozk and Fisher', 'Yundt, Johns and Cole', 'Hintz Inc',
       'Boyle, Price and Jacobson', 'Prosacco LLC',
       'Hamill, Walsh and Volkman', 'Stamm LLC', 'Prohaska-Shanahan',
       'Funk, Marks and Zboncak', 'Greenholt and Sons', 'Blick-Farrell',
       'Stanton, Haley and Ruecker', 'Harber, Runte and Glover',
       'Kohler-Zieme', 'Ernser, Nolan and Marquardt', 'Kreiger and Sons']
App_feature = 'Approving_officer'
Req_feature = 'Requesting_officer'
Supp_feature = 'Supplier_Name'

app = Flask(__name__)

def Single_Features_fraud_count(Feature_name1,feature_value1):
    tot_trans = 0
    fraud_trans = 0
    for i in range(4000):
        if data[Feature_name1].iloc[i] == feature_value1 :
            tot_trans = tot_trans + 1

            if data.Fraud.iloc[i] == 1 :
                fraud_trans = fraud_trans + 1

    return tot_trans,fraud_trans

# prediction function
def ValuePredictor(to_predict_list):
        to_predict = np.array(to_predict_list).reshape(1,13)
        loaded_model = pickle.load(open("DT_model.pkl", "rb"))
        result = loaded_model.predict(to_predict)
        return result[0]
    
        

@app.route('/')
def hello():
    return render_template("index3.html")

@app.route('/result', methods = ['POST'])
def result():
	if request.method == 'POST':
            to_predict_list = request.form.to_dict()
            to_predict_list = list(to_predict_list.values())

            App_off_in = App_Officers[int(to_predict_list[0])]
            Req_off_in = Req_Officers[int(to_predict_list[1])]
            supp_in = Suppliers[int(to_predict_list[2])]
            app_tot_trans,app_fraud_trans = Single_Features_fraud_count(App_feature,App_off_in)
            Req_tot_trans,Req_fraud_trans = Single_Features_fraud_count(Req_feature,Req_off_in)
            supp_tot_trans,supp_fraud_trans = Single_Features_fraud_count(Supp_feature,supp_in)
            # Drawing Graphs
            img1,img2 = draw_graphs(App_off_in,Req_off_in,supp_in)

            d1 = to_predict_list[7]
            d2 = to_predict_list[8]
            d3 = to_predict_list[9]
            d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
            d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
            d3 = datetime.datetime.strptime(d3, "%Y-%m-%d")

            try:
                days_for_submit = d2 - d1
                days_for_submit = str(days_for_submit)
                days_for_submit = days_for_submit.split()[0]
                days_for_submit = int(days_for_submit)
            except ValueError:
                days_for_submit = 0

            try:
                diff = d3 - d2
                diff = str(diff)
                diff = diff.split()[0]
                diff = int(float(diff))
            except ValueError:
                diff = 0

            to_predict_list.append(days_for_submit)
            to_predict_list.append(diff)
            to_predict_list.pop(7)
            to_predict_list.pop(7)
            to_predict_list.pop(7)

            result = ValuePredictor(to_predict_list)	
            if int(result)== 1:
                prediction = 'Fraud Happened'
            elif int(result) == 0:
                prediction ='Fraud Not Happened'

            print(type(result))
            return render_template("result.html",Req_off_in=Req_off_in,supp_in=supp_in, App_off_in = App_off_in, prediction = prediction, app_fraud_trans = app_fraud_trans, app_tot_trans=app_tot_trans, Req_tot_trans=Req_tot_trans, Req_fraud_trans=Req_fraud_trans,supp_tot_trans=supp_tot_trans,supp_fraud_trans=supp_fraud_trans,img_data1=img1,img_data2=img2)

if __name__ == '__main__':
    app.run(debug=True)