def jwt_required(func):
    def wrapper(*args, **kwargs):
        from flask import redirect, session, request
        from flask_jwt_extended import decode_token
        from datetime import datetime
        # attempt to grab the jwt from request
        try:
            token = session.get("access_token", None)
        except:
            token = None
        jwt_data = decode_token(token) if token != None else None
        # if the grab worked and the identity key is in the dict then proceed
        if jwt_data and jwt_data.get("exp", 0) >= int(datetime.now().strftime('%s')):
            return func(*args, **kwargs)
        else:
            return redirect(f'/login?msg=Require Login&rurl={request.path}', code=302)
    return wrapper


def get_user():
    from flask import session
    from flask_jwt_extended import decode_token
    try:
        token = session.get("access_token", None)
    except:
        token = None
    jwt_data = decode_token(token) if token != None else None
    if jwt_data == None:
        return (None, None, None)
    return tuple(jwt_data.get("sub").split(";"))
