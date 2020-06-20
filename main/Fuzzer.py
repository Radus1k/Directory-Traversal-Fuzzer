import random
import tkinter
import json
import concurrent.futures
import fuzzing_vars as fv

from requests import RequestException
import requests
from requests import cookies
import collections
from matplotlib import pyplot as plt
import re
from pdf_Generator import write_to_pdf
import crawl_links
import time
from DB import DatabaseConnection
from DB import copy_db_to_android


def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


'''  This function s vulnerables links '''
successful_headers = list()
error_headers = list()
successful_texts = list()

req_Session = requests.session()


class FuzzEngine:
    def __init__(self, url, port, cookie, module, save_results, payloads, check_crawl_links, shell_file, check_https,
                 quite_mode, gui_proxy, threads_no, method, username, password, header_list):
        self.url = url
        self.http_headers = header_list
        self.dbConn = DatabaseConnection()
        self.plot_x = []  # time
        self.plot_y = []  # founded vulnerabilties
        self.plot_y_attempts = []
        self.start = int(round(time.time()))
        self.attempts = int(0)
        self.port = port
        # self.cookie = cookie
        self.cookie = self.set_cookie_for_DWVA()
        self.payloads = payloads
        self.https_check = check_https
        self.method = method
        self.threads_no = threads_no
        self.proxy = gui_proxy
        self.payload_content = list()  # list of strings for every payload file
        self.faults = int(0)
        self.admin = username
        self.password = password
        self.responses_list = list()
        self.dots_exploitable = fv.dots_exploitable
        self.slashes_exploitable = fv.slashes_exploitable
        self.Special_Prefix_Patterns = fv.Special_Prefix_Patterns
        self.Special_Prefixes = fv.Special_Prefixes
        self.Special_Mid_Patterns = fv.Special_Mid_Patterns
        self.Special_Sufixes = fv.Special_Sufixes
        self.Special_Patterns = fv.Special_Patterns

        self.proxy_path = "proxy-list/proxy-list.txt"
        # self.payload_def_path = "Payloads/File Inclusion/Intruders/List_Of_File_To_Include_NullByteAdded.txt"
        self.payload_def_path = "Payloads/File Inclusion/Intruders/Web-files.txt"
        self.max_directories_depth = 5

        self.port = port
        # self.cookie = cookie
        self.module = module
        self.save_results_bool = save_results
        self.payloads_files = payloads
        self.check_craw_links = check_crawl_links
        self.shell_file = shell_file
        self.check_HTTPS = check_https
        self.check_quite_mode = quite_mode
        self.full_url = self.get_full_url(self.url, self.module)
        self.fuzzer_paused = False
        self.fuzz_counter = 0


    def get_url_indexes_to_inject(self):
        indexes = list()
        regex = re.compile('file=|page=|index.php')
        match = regex.search(self.full_url)
        try:
            if match.end(0) != -1:
                indexes.append(match.end(0))
            if match.end(1) != -1:
                indexes.append(match.end(1))
            if match.end(2) != -1:
                indexes.append(match.end(2))
        finally:
            last_bracket = self.full_url.rfind("/")
            if last_bracket > 6:  # other than http://
                indexes.append(last_bracket)
            else:
                indexes.append(len(self.full_url))
            return indexes

    def extract_payloads(self):
        for payload_path in self.payloads:  # self.payloads its a list of filenames containing the malitious input
            if payload_path == "Default Payload":
                payload_path = self.payload_def_path
            with open(payload_path, encoding='utf-8') as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            self.payload_content.append(content)

    def pause_fuzzing(self):
        self.fuzzer_paused = True

    def resume(self, root):
        self.fuzzer_paused = False
        self.get_request_status(self.full_url, root)

    def start_fuzzing(self, root):
        # rand_proxy = args.randproxy
        # cookie = set_cookie_for_DWVA(cookie)
        self.extract_payloads()
        # if rand_proxy is True:
        # proxy = get_rand_proxy, module)
        login_to_Site()
        self.set_http_headers()
        self.fuzz_Engine(root)
        # print(self.threads_no)
        write_to_pdf(self.plot_x, self.plot_y)
        self.dbConn.my_cursor.close()
        self.dbConn.connection.close()
        # copy_db_to_android()

    def getFaults(self):
        return self.faults

    def inject_dt(self, full_url):
        full_url = full_url.partition("\n")[0]
        indexes = self.get_url_indexes_to_inject()
        payloads = flatten(self.payload_content)
        url_vulnerables = list()
        for index in indexes:
            if index != -1:
                for payLoad in payloads:
                    url_bad = full_url[:index + 5] + payLoad
                    url_vulnerables.append(url_bad)
        return url_vulnerables

    def send_request(self, url):
        self.attempts = self.attempts + 1
        # self.plot_y_attempts.append(self.attempts)
        # self.plot_y.append(self.faults)
        # self.plot_x.append(int(round(time.time())) - self.start)

        try:
            if self.method == "GET":
                req_Session = requests.get(url, cookies=self.cookie, proxies=self.proxy, timeout=0.1)

            if self.method == "POST":
                req_Session = requests.post(url, cookies=self.cookie, proxies=self.proxy, timeout=0.1)

            successful_headers.append(req_Session.url + "\n" + str(req_Session.headers))
            req_text = req_Session.text
            successful_texts.append(req_Session.url + "\n" + req_text)
            # if req_Session.status_code == 200:

            # successful_headers.append(str(req_Session.url) + "\n" + str(req_Session.headers))
            # error_headers.append(str(req_Session.url) + "\n" + str(req_Session.headers))

            if req_Session.status_code != 200:
                # if req_text.find("Failed opening") > 0 or req_text.find("such") > 0 or req_text.find("Error") > 0:
                self.faults = self.faults + 1
                self.plot_x.append(self.faults)
                self.plot_y.append(int(round(time.time())) - self.start)
                # return req_Session.status_code
            # if req_text not in self.responses_list:
            #   #self.responses_list.append(req_text)
            # else:
            #   return 404
            return req_Session.status_code
        except Exception as e:
            print("error at request")
            if str(e).find("Read timed out") != -1:
                return 408  # timeout
        return req_Session.status_code

    def fuzz_Engine(self, root):
        full_url = self.get_full_url(self.url, self.module)
        if self.check_craw_links == 1:
            fuzzed_urls = self.inject_dt(full_url)
            self.get_request_status(fuzzed_urls, root)
            crawled_links = crawl_links.getAllUrl(full_url)
            for crawled in crawled_links:
                injected_list = self.inject_dt(crawled)
                self.get_request_status(injected_list, root)
        else:
            fuzzed_urls = self.inject_dt(full_url)
            self.get_request_status(fuzzed_urls, root)

    def get_request_status(self, fuzzed_urls, root):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads_no) as executor:
            url_list = {executor.submit(self.send_request, url): url for url in fuzzed_urls[self.fuzz_counter:]}
            for future in concurrent.futures.as_completed(url_list):
                fuzzed = url_list[future]
                try:
                    status = future.result()
                    if not self.fuzzer_paused:
                        self.fuzz_counter = self.fuzz_counter + 1
                        self.dbConn.send_values([self.full_url, fuzzed, status, len(fuzzed)])
                        if self.check_quite_mode == 0:
                            root.addrow(status, fuzzed, len(fuzzed))

                            tkinter.Frame.update(root)
                        elif self.check_quite_mode == 1 and status == 200:
                            root.addrow(status, fuzzed, len(fuzzed))
                            tkinter.Frame.update(root)
                        else:
                            break
                    else:
                        break

                except Exception as e:
                    print(e)

    def get_full_url(self, url, module):
        if len(self.port) < 2:
            if url.find("http:") == -1:
                return module + "://" + self.url
            else:
                return self.url
        else:
            if url.find("http:") == -1:
                return module + "://" + self.url + ":" + str(self.port) + "/"
            else:
                return self.url + ":" + str(self.port) + "/"

    '''Set cookies params from a long string by splitting it '''

    def set_cookies(self, string):
        keys_and_values = string.split()
        self.cookie = requests.cookies.RequestsCookieJar()
        for k in keys_and_values:
            self.cookie.set(k.split('=')[0], k.split('=')[1])
        return self.cookie

    @staticmethod
    def set_cookie_for_DWVA():
        cookie = requests.cookies.RequestsCookieJar()
        security = 'security'
        security_value = 'medium'
        session = 'PHPSESSID'
        # response = requests.post('http://127.0.0.1/dvwa/login.php',
        #                        data={'username': 'admin', 'password': 'password', 'Login': 'Login'})
        session_value = '0ndt9teo4bv2qteja0uo5fqkjs'
        cookie.set(security, security_value)
        cookie.set(session, session_value)
        return cookie

    ''' Generate random proxy from list'''

    def get_rand_proxy(self):
        rand = random.randrange(10, 310)
        with open(self.proxy_path) as f:
            lines = f.readlines()
            line_proxy = lines[rand + 1]
        proxyDict = {"http": self.module + "://" + line_proxy.split()[0],
                     "https": self.module + "://" + line_proxy.split()[0]
                     }
        return proxyDict

    def set_http_headers(self):
        headers_tuple = {}
        for tuple_ in self.http_headers:
            headers_tuple[tuple_[0]] = tuple_[1]
        req_Session.headers = headers_tuple


def get_iplist_from_file(filename):
    with open(filename) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    return content


def write_response(req, filename):
    with open(filename, "w") as f:
        f.write(str(req, 'utf8'))
        f.write('\n\n\n')
        f.close()


def login_to_Site():
    login_payload = {
        'username': 'admin',
        'password': 'password',
        'Login': 'Login'
    }
    try:
        response = req_Session.get('http://127.0.0.1:8080/DVWA-master/login.php')
        token = re.search("user_token'\s*value='(.*?)'", response.text).group(1)
        login_payload['user_token'] = token
        p = req_Session.post('http://127.0.0.1:8080/DVWA-master/login.php', data=login_payload)
    except:
        print("cannot log in")
    finally:
        print("Logged in!")

