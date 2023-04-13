import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas
import pickle
import json

dflaminates=pickle.load(open("royaletouche_pkl.pkl","rb"))
#dflaminates=dflaminates['assigned_value'].values
sig = pickle.load(open('sigx','rb'))
indices = pickle.load(open('indicesx','rb'))

class model_input(BaseModel):
    assigned_value: int


app = FastAPI()

@app.get('/')
def index():
    return{'message':'hello'}

@app.post('/Welcome')
def get_name(name:str):
    return {'welcome yaar':f'{name}'}

@app.get("/predict/{assigned_value}")
async def read_item(assigned_value):
    idx = indices[int(assigned_value)]
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1:6]
    laminate_indices = [i[0] for i in sig_scores]
   
    #results = dflaminates[182]
    results =  dflaminates['assigned_value'].iloc[laminate_indices]
    #pred = dflaminates.predict([model_input])

    print('array of assigned values:',laminate_indices)
    responsedata = results.to_json()

    xyz = json.loads(responsedata)

    return xyz


@app.post('/predict')
def recommend(data:model_input):
    idx = indices[data.assigned_value]
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1:6]
    laminate_indices = [i[0] for i in sig_scores]
   
    #results = dflaminates[182]
    #results = dflaminates.iloc[laminate_indices]
    results = dflaminates['assigned_value'].iloc[laminate_indices]
    #pred = dflaminates.predict([model_input])

    #print('array of assigned values:',laminate_indices)
    print('laminates',results.to_json())

    return str(results)

    #print('id',idx)
    #return data





if __name__=='__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

#uvicorn api_royale:app --reload
