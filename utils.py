def _param_update(old_params, new_params):
    args, kwargs = old_params

    if type(new_params) == tuple:
        if len(new_params) == 2 and type(new_params[0]) == tuple and type(new_params[1]) == dict:
            args = new_params[0]
            kwargs.update(new_params[1])
        else:
            args = new_params
    elif type(new_params) == dict:
        kwargs.update(new_params)

    return (args, kwargs)

def filter_dict(d, fltr):
    return dict( (x, d[x]) for x in fltr if x in d )
        
def apply_some(f, *args, **kwargs):
    fspec = getargspec(f)
    return f(*args, **kwargs) if fspec.keywords else f( *args, **filter_dict(kwargs, fspec.args) )