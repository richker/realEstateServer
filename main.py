from flask import Flask
from flask import request
import pandas as pd
import joblib
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def insertValues(df, input_dic):
    df.at[0,'year_of_construction'] = input_dic['year_of_construction']
    df.at[0,'floor']                = input_dic['floor']
    df.at[0,'shetachneto']          = input_dic['shetachneto']
    df.at[0,'floors']               = input_dic['floors']
    df.at[0,'year']                 = input_dic['year']
    df.at[0,'month']                = input_dic['month']
    df.at[0,'day']                  = input_dic['day']
    # if (input_dic['model'] != "Random Forest - No Soceco"):
    df.at[0,'soceco']               = input_dic['soceco']
    df.at[0,'dirotbnyn']               = input_dic['apartments']
    df.at[0,'type_בית בודד']          = 0
    df.at[0,'type_דירה בבית קומות']    = 0
    df.at[0,'type_דירת גג']           = 0
    df.at[0,'type_דירת גן']           = 0
    df.at[0,'type_דירת דופלקס']        = 0
    df.at[0,"type_קוטג' דו-משפחתי"]    = 0
    df.at[0,"type_קוטג' טורי"]         = 0
    for item in df:
        if "type" in item:
            print("item")
            print(item)
            if input_dic['type'] in item:
                df.at[0, 'type_בית בודד'] = 1
    return df

def parse_gush_parameter(df, gush_str):
    for feature in df:
        if "gush_" in feature:
            if gush_str in feature:
                df.at[0,feature]  = 1
            else:
                df.at[0,feature]  = 0
    return df


@app.route('/', methods=['POST'])
def compute_price():
    dict_res = request.get_json()
    print("dict_res", dict_res)
# loading model
    if (dict_res['model'] == "Random Forest"):
        loaded_model = joblib.load('RandomForestRegressor_model.pkl')
    elif (dict_res['model'] == "Random Forest - No Soceco"):
        loaded_model = joblib.load('RandomForestRegressor_model_no_soceco.pkl')
    else:
        loaded_model = joblib.load('LinearRegression.pkl')
# loading dataframe by
    if (dict_res['model'] == "Random Forest - No Soceco"):
        df = pd.read_csv('dataframe_row.csv')
    else:
        df = pd.read_csv('dataframe_row.csv')
    df = insertValues(df, dict_res)
    df = parse_gush_parameter(df, dict_res['gush'])
    result = loaded_model.predict(df)
    print("****** RESULT: ")
    result_list = result.tolist()
    result_price = int(result.tolist()[0])
    return str(result_price)

if __name__ == '__main__':
    app.run(debug = True)