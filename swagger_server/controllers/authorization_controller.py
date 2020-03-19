from typing import List
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_geosys_auth(token):


    #return {'scopes': ['read', 'write', 'delete'], 'uid': '1234567890'}
    return {'scopes': ['read', 'write', 'delete']}

def validate_scope_geosys_auth(required_scopes, token_scopes):
    
    return set(required_scopes).issubset(set(token_scopes))
    


