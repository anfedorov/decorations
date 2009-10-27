# Python Decorations

Decorations are great! They help you not repeat yourself, abstract functionality, and write simple code. This module makes it easy to write clean, readable, decorations.

## Philosophy
Decorations themselves have a lot of "cruft" that can be abstracted away. Several attempts have been made at fixing this, the most evolved of which I've found to be [the decorator module](http://pypi.python.org/pypi/decorator/). This project is an evolution on the same abstractions.

## Design Goals

There are two main design goals this module addresses.

### Two common classes of decorations

Of all the decorations I've come across, many fall into two categories: those that execute before the decorated method (and possibly edit arguments), and those that execute after the decorated method (and possibly edit return values). These are exposed as:

    @predecoration
    def acceptsGET(f, args):
        if len(args) == 1:
            fargs = inspect.getargspec(f).args
            get = args[0].GET
            return util.filter_dict(get, fargs[1:])
    
    @acceptsGET
    def my_django_view(request, some_get_var, other_get_var):
        # ...
        
means that POST variables called some_get_var or other_get_var will be passed as arguments right into your view, *but* calls to...
    
    my_django_view(r, 10, 20)
    
...will bypass the predecoration.

postdecorations work similarly (TODO: postdecoration example).

### Decorations with parameters

Often, decorations that initially had no parameters need to be extended to include parameters. This poses several problems:

First, extending the decoration naively breaks all current uses of the decoration.
Second, it requires quite intricate changes to the decorator - an extra closure must be added to capture the decorator arguments.

#### Decorations to the rescue!

Functions which have been decorated with @predecoration have at most five arguments. The first is the function being decorated. The other four are keyword arguments: args, kwargs, dec\_params and dec\_kwargs.

    @predecoration
    def foo(f, args, kwargs, dec_params, dec_kwargs):
        # ...
    
    @foo
    def bar(c, d):
        # ...
    
    @foo(1, 2, a=3, b=4)
    def baz(c, d, e, f):
        # ...

so when when you call bar(5, 6, e=7, f=8), foo will be pre-processed with

    f == bar
    args == [5, 6]
    kwargs == {'e': 7, 'f': 8}
    dec_params = None
    dec_kwargs = None
    
but when you call baz(5, 6, e=7, f=8), foo will pre-process with:

    f == bar
    args == [5, 6]
    kwargs == {'e': 7, 'f': 8}
    dec_params = [1, 2]
    dec_kwargs = { 'a': 3, 'b': 4 }
    
The predecoration is doesn't need to change!
