

def dict_helper(objlist):
    results = [item.serialize for item in objlist]
    return results

class CustomException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code