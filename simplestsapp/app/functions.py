from typing import Union
from flask import session
import requests

def check_bearer_token(data_session: session) -> bool:

    if 'access_token' not in data_session:
        return False
    
    return True
    
def get_client_id(api_url: str, bearer_token: str) -> Union[int, None]:

    response = requests.get(api_url + 'user/', 
                                    headers={'Authorization': f'Bearer {bearer_token}'}
                                    ).json()
    
    if 'client_id' not in response:
        return None
    
    return response['client_id']