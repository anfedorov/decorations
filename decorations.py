# python
from functools import wraps, partial
from inspect import getargspec

# local
from utils import *

def _metadecorator(decoration, params="maybe"):
    "Takes a decoration to pre-apply to a decoratee"
    def cap_params(*dec_params, **dec_kwargs):
        "Captures decoration parameters"
        @wraps(decoration)
        def decorator(decoratee):
            "The decorator - takes a decoratee to decorate"
            @wraps(decoratee)
            def decorated(*args, **kwargs):
                "The decorated decoratee"
                # the decoration will be passed the decoratee and (optionally) two sets of arguments
                return apply_some(decoration, decoratee, args=args, kwargs=kwargs, dec_params=dec_params, dec_kwargs=dec_kwargs)
            return decorated
        
        if params=="maybe" and not dec_kwargs and len(dec_params)==1 and callable(dec_params[0]):
            decoratee = dec_params[0]
            dec_params = ()
            return decorator(decoratee)
        else:
            return decorator
            
    return cap_params

def decoration(decoration=None, has_params="maybe"):
    "Meta-decorates"
    if decoration:
        dec_args = getargspec(decoration).args
        if 'dec_params' in dec_args or 'dec_kwargs' in dec_args:
            return _metadecorator(decoration, params=has_params)
        else:
            return _metadecorator(decoration, params=has_params)()
    else:
        return partial(decoration, params=has_params)

@decoration
def predecoration(f, args, kwargs):
    "Declares something as a predecoration"
    def predecorator(g, **kwds):
        # at this point, `f` will be our predecoration and `g` will be our decoratee.
        update = apply_some(f, g, **kwds)
        gargs, gkwargs = _param_update((kwds['args'], kwds['kwargs']), update)
        return g(*gargs, **gkwargs)
    return _metadecorator(predecorator)(*args, **kwargs)

@decoration
def postdecoration(f, args, kwargs, dec_kwargs):
    "Declares something as a postdecoration"
    def postdecorator(g, **kwds):
        # at this point, `f` will be our postdecoration and `g` will be our decoratee.
        res = g(*kwds['args'], **kwds['kwargs'])
        return apply_some(f, res, *kwds['dec_params'], **kwds['dec_kwargs'])
    return _metadecorator(postdecorator, dec_kwargs.get('has_params', 'maybe'))(*args, **kwargs)
