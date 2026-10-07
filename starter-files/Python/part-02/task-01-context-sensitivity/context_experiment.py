from typing import Dict, Any, List

def transformationdata(data: List[Dict[str, Any]]) -> List[str]:
    # TODO Extract the 'name' field from each dictionary and return as a list of strings
    return [item['name'] for item in data]









