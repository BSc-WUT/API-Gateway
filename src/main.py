from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List
import requests
import os
import json

from .models import Model, NetworkFlow, NetworkFlowFull



def get_env_vars() -> dict:
    load_dotenv()
    return {
        "DB_API_URL": f'http://{os.getenv("DB_API")}:{os.getenv("DB_API_PORT")}',
        "ML_API_URL": f'http://{os.getenv("ML_API")}:{os.getenv("ML_API_PORT")}',
        "API_PORT": os.getenv('API_PORT'),
    }


app = FastAPI()
ENV_VARS = get_env_vars()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


""" ML API """


@app.get('/models')
def get_models() -> JSONResponse:
    response: requests.Response = requests.get(f"{ENV_VARS['ML_API_URL']}/models")
    result: dict = response.json()
    models: List[Model] = result
    return models


@app.get('/models/{model_name}')
def get_model(model_name: str) -> JSONResponse:
    response: requests.Response = requests.get(f"{ENV_VARS['ML_API_URL']}/models/{model_name}")
    result: dict = response.json()
    models: Model = result
    return models


@app.get('/models/activate/{model_name}/activate')
def activate_model(model_name: str) -> JSONResponse:
    response: requests.Response = requests.get(f"{ENV_VARS['ML_API_URL']}/models/activate/{model_name}")
    result: dict = response.json()
    return result


@app.get('/models/deactivate/{model_name}')
def deactivate_model(model_name: str) -> JSONResponse:
    response: requests.Response = requests.get(f"{ENV_VARS['ML_API_URL']}/models/deactivate/{model_name}")
    result: dict = response.json()
    return result


@app.post('/models/predict/{model_name}')
def predict(model_name: str, flow: NetworkFlow) -> JSONResponse:
    response: requests.Response = requests.post(f"{ENV_VARS['ML_API_URL']}/models/predict/{model_name}", data=json.dumps(flow.dict()))
    result: dict = response.json()
    return result


@app.delete('/models/delete/{model_name}')
def delete_model(model_name: str) -> JSONResponse:
    response: requests.Response = requests.delete(f"{ENV_VARS['ML_API_URL']}/models/delete/{model_name}")
    result: dict = response.json()
    return result


@app.post('/models/upload')
def upload_model(file: UploadFile) -> JSONResponse:
    files: dict = {'upload_file': (file.filename, file.file, file.content_type)}
    response: requests.Response = requests.post(f"{ENV_VARS['ML_API_URL']}/models/{file.filename}/upload", files=files)
    result: dict = response.json()
    return result


""" DB_API """


@app.get('/network_flows')
def get_flows() -> List[NetworkFlowFull]:
    response: requests.Response = requests.get(f"{ENV_VARS['DB_API_URL']}/network_flows")
    flows: List[NetworkFlowFull] = [dict({'id': hit.get('_id')}, **hit.get('_source', {})) for hit in response.json().get('hits', {}).get('hits', [])]
    return flows


@app.get('/network_flows/{flow_id}')
def get_flow(flow_id: str) -> JSONResponse:
    response: requests.Response = requests.get(f"{ENV_VARS['DB_API_URL']}/network_flows/{flow_id}")
    try:
        flow: NetworkFlow = response.json()
    except Exception:
        flow: dict = {}
    return flow


@app.put('/network_flows/{flow_id}')
def update_flow(flow_id: str, flow: NetworkFlowFull) -> JSONResponse:
    response: requests.Response = requests.put(f"{ENV_VARS['DB_API_URL']}/network_flows/{flow_id}", data=json.dumps(flow.dict()))
    result: dict = response.json()
    return result
