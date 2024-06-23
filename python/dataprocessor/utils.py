def helper(*args, **kwargs):
    return kwargs

def get_variable_name(**kwargs):
    for variable_name in kwargs:
        print(variable_name)