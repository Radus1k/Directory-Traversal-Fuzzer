import os
import sys
import argparse
import requests
from http.cookies import SimpleCookie
from requests import cookies
import createRequests
from argparse import ArgumentParser


def menu():
    parser = ArgumentParser(description="Choose option for fuzzing test", formatter_class=argparse.RawTextHelpFormatter,
                            epilog="For more details use the README file", add_help=True)

    parser.add_argument('-m', "--module", type=str, default='http', choices=['http', 'https', 'FTP', 'tftp', 'payload']
                        , help="Specify the module. Available options:"
                               "Http / Https / FTP / payload / tftp",
                        metavar='', required=False)

    parser.add_argument('-p', "--port", type=str, default=80, help="Specify the target port",
                        metavar='', required=False)

    parser.add_argument('-u', "--url", type=str, default=None, help="Specify the site name",
                        metavar='', required=False)

    parser.add_argument('-i', "--ip", type=str, default=None, help="Specify the target IP or type 'lh' for 127.0.0.1",
                        metavar='', required=False)

    parser.add_argument('-g', "--method", choices=['GET', 'POST'],
                        help="Specify request type ('GET' or 'POST')",
                        default='GET', metavar='', required=False)

    parser.add_argument('-f', "--file", type=str, default=None, help="Specify file containing urls",
                        metavar='', required=False)

    parser.add_argument('-c', '--cookie', type=str,
                        default=None, help="Add Cookie within the request"
                                           "Example of correct input: key1:value1 key2:value2")

    parser.add_argument('-o', "--output", type=str, default=None, help="Output the fuzz process test in console")

    parser.add_argument('-ua', '--useragent',
                        default=None, help='Adding fake user agents')

    parser.add_argument('-q', '--randproxy',
                        default=None, type=bool, help='Add random proxy (ip/port/code')

    parser.add_argument('-pp', '--proxy',
                        default=None, type=str, help='Add specific proxy (ip/port/code')

    ''' If no arguments, print help again  '''
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.print_usage()
        parser.exit()
    args = parser.parse_args()
    return args


def set_cookie_for_DWVA(cookie_string):
    if cookie_string is None:
        cookie = requests.cookies.RequestsCookieJar()
        security = 'security'
        security_value = 'medium'
        session = 'PHPSESSID'
        session_value = 'varglhsfc0fpa3h6k1tuff7kp2'
        cookie.set(security, security_value)
        cookie.set(session, session_value)
    else: # User set some input
        cookie = get_cookie(cookie_string)
    return cookie


def send_request():
    args = menu()
    url = args.url
    port = args.port
    module = args.module
    cookie = args.cookie
    cookie = set_cookie_for_DWVA(cookie)
    ip = args.ip
    if ip == "lh":
        ip = "127.0.0.1"

    method = args.method
    proxy = args.proxy
    if url is None:
        url = ""
    if ip:
        fullUrl = str(module) + "://" + str(ip) + ":" + str(port) + "/" + str(url)
    else:
        fullUrl = module + "://" + str(url) + ":" + str(port)
    try:
        if method == "GET":
            req = requests.get(fullUrl, cookies=cookie, proxies=proxy, timeout=2)
            print(req.cookies)
        else:
            req = requests.post(fullUrl, cookies=cookie, proxies=proxy, timeout=2)
        write_response(req)
    except Exception as e:
        print("Failed to establish connection")
        print(e)
    finally:
        print("Ok")


def write_response(req):
    with open("request.html", "w") as f:
        f.write(str(req.content, 'utf8'))


def get_cookie(string):
    keys_and_values = string.split()
    cookie = requests.cookies.RequestsCookieJar()
    for k in keys_and_values:
        print(k.split('=')[0])
        print(k.split('=')[1])
        cookie.set(k.split('=')[0], k.split('=')[1])
    return cookie


def main():
    send_request()


if __name__ == "__main__":
    main()
