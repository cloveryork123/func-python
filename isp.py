"""Fetch info from the short url click"""
try:
    # Optional package
    import os
    import geoip2.database
except Exception:
    print("ModuleNotFoundError: No module named 'geoip2'")

def parse_request(request):
    """Pass request object and returns parsed data dict.
    Country is fetched from IP using maxmind db.

    :param request:
    :return:
    """
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    data = dict(
        referrer=request.referrer,
        user_agent=request.headers.get("User-Agent"),
        country=ip_country(ip)
    )
    return data

def parse_header(request):
    """Pass request object and returns parsed data dict.
    Country is fetched from IP using maxmind db.

    :param request:
    :return:
    """
    ip = request.headers.get('Pygmy-App-User-Ip')
    data = dict(
        referrer=request.headers.get('Pygmy-Http-Rreferrer'),
        user_agent=request.headers.get('Pygmy-Http-User-Agent'),
        country=ip_country(ip)
    )
    return data

def ip_country(ip):
    """Get country from ip. Uses Geoip2 db.

    :param ip:
    :return: None/str
    """
    c_iso_code = None
    try:
        db_path = './utils/GeoLite2-Country.mmdb'
        if os.getcwd().find('utils') > 0:
            db_path = './GeoLite2-Country.mmdb'
        if os.path.exists(db_path):
            reader = geoip2.database.Reader(db_path)
            c = reader.country(ip)
            c_iso_code = c.country.iso_code
        else:
            print(f"ERROR: {db_path} does not exist.")
    except Exception as e:
        print(f"ERROR: {str(e)}")
    return c_iso_code

def ip_score(timestamp) -> float:
    # print("timestamp:", timestamp)
    score = 0.0
    if timestamp >= 100000:
        score = 10.0 - timestamp/10000
    elif timestamp >= 10000:
        score = 20.0 - timestamp/900
    elif timestamp >= 1000:
        score = 70.0 - timestamp/180
    elif timestamp >= 100:
        score = 90.0 - timestamp/45
    else:
        score = 100.0 - timestamp/9
    
    if score < 0:
        score = 0
    return round(score, 2)
