import json
import requests
import os
from dotenv import load_dotenv
from typing import Any, Dict


class PacketBaseClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_models(self) -> Dict[str, Any]:
        response = requests.get(f"{self.api_url}/models")
        return response.json()

    def get_model(self, model_name: str) -> Dict[str, Any]:
        response = requests.get(f"{self.api_url}/models/{model_name}")
        return response.json()

    def activate_model(self, model_name: str) -> Dict[str, Any]:
        response = requests.get(f"{self.api_url}/models/activate/{model_name}")
        return response.json()

    def deactivate_model(self, model_name: str) -> Dict[str, Any]:
        response = requests.get(f"{self.api_url}/models/deactivate/{model_name}")
        return response.json()

    def predict(self, model_name: str, flow: Dict) -> Dict[str, Any]:
        response = requests.post(f"{self.api_url}/models/predict/{model_name}", json=flow)
        return response.json()

    def delete_model(self, model_name: str) -> Dict[str, Any]:
        response = requests.delete(f"{self.api_url}/models/delete/{model_name}")
        return response.json()

    def upload_model(self, file: Dict) -> Dict[str, Any]:
        response = requests.post(f"{self.api_url}/models/upload", files=file)
        return response.json()

    def get_flows(self) -> Dict[str, Any]:
        response = requests.get(f"{self.api_url}/network_flows")
        return response.json()

    def get_flow(self, flow_id: str) -> Dict[str, Any]:
        response = requests.get(f"{self.api_url}/network_flows/{flow_id}")
        return response.json()

    def update_flow(self, flow_id: str, flow: Dict) -> Dict[str, Any]:
        response = requests.put(f"{self.api_url}/network_flows/{flow_id}", json=flow)
        return response.json()


''' COMMAND FUNCTIONS '''

def get_models_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    result = client.get_models()
    return CommandResults(readable_output=str(result), outputs=result)

def get_model_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    model_name = args.get("model_name")
    result = client.get_model(model_name)
    return CommandResults(readable_output=str(result), outputs=result)

def activate_model_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    model_name = args.get("model_name")
    result = client.activate_model(model_name)
    return CommandResults(readable_output=str(result), outputs=result)

def deactivate_model_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    model_name = args.get("model_name")
    result = client.deactivate_model(model_name)
    return CommandResults(readable_output=str(result), outputs=result)

def predict_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    model_name = args.get("model_name")
    flow = args.get("flow")
    result = client.predict(model_name, flow)
    return CommandResults(readable_output=str(result), outputs=result)

def delete_model_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    model_name = args.get("model_name")
    result = client.delete_model(model_name)
    return CommandResults(readable_output=str(result), outputs=result)

def upload_model_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    file = args.get("file")
    result = client.upload_model(file)
    return CommandResults(readable_output=str(result), outputs=result)

def get_flows_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    result = client.get_flows()
    return CommandResults(readable_output=str(result), outputs=result)

def get_flow_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    flow_id = args.get("flow_id")
    result = client.get_flow(flow_id)
    return CommandResults(readable_output=str(result), outputs=result)

def update_flow_command(client: PacketBaseClient, args: Dict[str, Any]) -> Dict[str, Any]:
    flow_id = args.get("flow_id")
    flow = args.get("flow")
    result = client.update_flow(flow_id, flow)
    return CommandResults(readable_output=str(result), outputs=result)



''' MAIN FUNCTION '''


def main():
    params = demisto.params()
    args = demisto.args()
    command = demisto.command()

    load_dotenv()
    api_url = os.getenv("API_URL")

    client = PacketBaseClient(api_url)

    if command == 'packetbase-get-models':
        return_results(get_models_command(client, args))
    elif command == 'packetbase-get-model':
        return_results(get_model_command(client, args))
    elif command == 'packetbase-activate-model':
        return_results(activate_model_command(client, args))
    elif command == 'packetbase-deactivate-model':
        return_results(deactivate_model_command(client, args))
    elif command == 'packetbase-predict':
        return_results(predict_command(client, args))
    elif command == 'packetbase-delete-model':
        return_results(delete_model_command(client, args))
    elif command == 'packetbase-upload-model':
        return_results(upload_model_command(client, args))
    elif command == 'packetbase-get-flows':
        return_results(get_flows_command(client, args))
    elif command == 'packetbase-get-flow':
        return_results(get_flow_command(client, args))
    elif command == 'packetbase-update-flow':
        return_results(update_flow_command(client, args))

if __name__ == "__main__":
    main()
