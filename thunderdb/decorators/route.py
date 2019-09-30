import re
import inspect


def route(route_path):
    """Custom route decorator used for HTTP requests

    An example of the decorator for a HTTP GET request:

        @route("/data/<key>")
        def do_GET(self, key):
            pass

    When a route_path is passed into this decorator, which
    inherits from BaseHTTPRequestHandler, we can grab the extra
    keyword args by matching the pattern in the route path.

    Note: The pattern name (e.g: <key>) must match the arg name (e.g: "key")
          in the function definition.
    """
    def decorate(func):
        def wrap_and_call(self, *args, **kwargs):
            route_regex = re.sub(r'(<\w+?>)', r'(?P\1.+)', route_path)
            route_pattern = re.compile("^{}$".format(route_regex))
            match = route_pattern.match(self.path)
            
            # If there is a match, we have to populate the kwargs
            # with the corresponding matched values
            if match: 
                matching_dict = match.groupdict()
                keys = match.groupdict().keys()

                if all(x in inspect.getfullargspec(func).args for x in keys):
                    for x in keys:
                        kwargs[x] = matching_dict[x]

            return func(self, *args, **kwargs)
        return wrap_and_call
    return decorate
