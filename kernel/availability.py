import requests

# lower than 25 in the Internet Freedom Index or OpenAI API is not available
unsupported_areas = ['CN', 'CU', 'RU', 'KP', 'IR', 'VN', 'VE', 'MM']


def get_ip():
    resp = requests.get('https://ifconfig.me')
    return resp.text.strip()


def get_geoip():
    ip = get_ip()
    resp = requests.get(f'https://ipinfo.io/{ip}/json')
    return resp.json()


def check_availability():
    geoip = get_geoip()
    if geoip['country'] in unsupported_areas:
        return False
    return True
