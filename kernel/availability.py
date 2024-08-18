import requests

unsupported_areas = ['CN', 'CU', 'RU', 'KP', 'IR', 'VN', 'VE', 'MM']
country = 'US'


def get_ip():
    resp = requests.get('https://ifconfig.me')
    return resp.text.strip()


def get_geoip():
    ip = get_ip()
    resp = requests.get(f'https://ipinfo.io/{ip}/json')
    return resp.json()


def check_availability():
    global country
    geoip = get_geoip()
    print(geoip)
    country = geoip['country']
    if geoip['country'] in unsupported_areas:
        return False
    return True
