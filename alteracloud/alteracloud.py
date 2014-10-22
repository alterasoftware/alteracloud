"""
.. module:: alteracloud
   :platform: Unix, Windows
   :synopsis: Python class interface to the Altera Cloud REST API.
      
Copyright (C) 2014-2015 Altera Corporation, San Jose, California, USA.
All rights reserved.

This source code is made available pursuant to the following license
agreement (“Agreement”).

BY ACCESSING, COPYING, INSTALLING OR USING THIS SOFTWARE IN SOURCE
CODE OR BINARY FORM, YOU AGREE TO BE BOUND BY THE FOLLOWING TERMS AND
CONDITIONS:

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files
(collectively, the "Software"), to use the Software for any purpose
without restriction, including the right to copy, modify, merge,
publish, distribute, prepare derivatives of, sublicense, and otherwise
use the Software alone or in any derivative version, copies of the
Software, provided that the above copyright notice appears in all
copies or portions of the Software, and this license is retained in
the Software documentation, whether alone or in any derivative
version.  Additionally, the Altera Corporation name shall not be used
in any advertising or publicity pertaining to the distribution of the
Software without the prior written permission of Altera.

ALTERA IS PROVIDING THE SOFTWARE "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT.   IN NO EVENT SHALL ALTERA OR THE AUTHORS OF THE 
SOFTWARE BE LIABLE TO YOU OR ANY OTHER USER OF THE SOFTWARE FOR ANY 
DIRECT, INDIRECT, INCIDENTAL, SPECIAL OR CONSEQUENTIAL  DAMAGES OR 
LOSSES WHATSOEVER AS A RESULT OF USING, MODIFYING, OR DISTRIBUTING THE 
SOFTWARE OR ANY DERIVATIVES THEREOF, WHETHER IN AN ACTION OR CLAIM OF 
CONTRACT, NEGLIGENCE, TORT OR OTHERWISE, ARISING
FROM  OR IN CONNECTION WITH THE SOFTWARE, ITS PERFORMANCE OR ITS  USE, 
EVEN IF ADVISED OF THE POSSIBILITY OF THE OCCURRENCE OF SUCH DAMAGES OR 
LOSSES ..


The license granted above will terminate automatically upon a breach
of its terms and conditions.

This agreement shall be governed by and interpreted in all respects by
the laws of the State of California, United States of America, but
excluding its conflict of laws provisions.  Nothing in this Agreement
shal be deemed to create a relationship or agency, partnership or
joint venture between you and Altera.  This Agreement does not grant
any permission to use any Altera trademark, logo, trade name or
service mark, for any reason, including to endorse or promote your
products or service, or the products and services of any third party.

CONTACTING ALTERA

You can contact Altera through one of the following ways:

Mail:
   Altera Corporation
   Applications Department
   101 Innovation Drive
   San Jose, CA 95134

Altera Website:
   www.altera.com

Online Support:
   www.altera.com/mysupport

Troubshooters Website:
   www.altera.com/support/kdb/troubleshooter

Technical Support Hotline:
   (800) 800-EPLD or (800) 800-3753
      7:00 a.m. to 5:00 p.m. Pacific Time, M-F
   (408) 544-7000
      7:00 a.m. to 5:00 p.m. Pacific Time, M-F

   From other locations, call (408) 544-7000 or your local
   Altera distributor.

The mySupport web site allows you to submit technical service
requests and to monitor the status of all of your requests
online, regardless of whether they were submitted via the
mySupport web site or the Technical Support Hotline. In order to
use the mySupport web site, you must first register for an
Altera.com account on the mySupport web site.

The Troubleshooters web site provides interactive tools to
troubleshoot and solve common technical problems.
"""

import json
import socket
import requests

try:
    from urlparse import urljoin
    from urllib import urlencode
except ImportError:
    from urllib.parse import urljoin
    from urllib.parse import urlencode


class ConnectionError(Exception):
    """
    Represents an exception for errors that occur due to connection
    problems or otherwise bad results from the server. Useful in an
    HTTP context. For instance, subclasses of RESTConnection should
    raise ConnectionError if they cannot make connections to servers
    (socket errros) or if the server returns 500 response code.
    """

    def __init__(self, message, code=None, url='unknown'):
        self.code = code
        self.url = url
        Exception.__init__(self, message)

    def __str__(self):
        err = Exception.__str__(self)
        if self.code:
            err += "; Response Code: " + str(self.code)
        if self.url:
            err += "; URL: " + str(self.url)
        return err 


class RequestsBase(object):

    def __init__(self, *args, **kwargs):
        self.proxies = {}

    def set_proxy(self, proxy):
        if proxy:
            self.proxies = {
                "http": proxy,
                "https": proxy,
            }
    
    def request_put(self, url, data=None):
        return self.request("put", url, data=data)

    def request_post(self, url, data=None):
        return self.request("post", url, data=data)

    def request_patch(self, url, data=None):
        return self.request("patch", url, data=data)

    def request_get(self, url, params=None):
        if params:
            query_string = urlencode(params)
            url = url + "?" + query_string

        return self.request("get", url, data=None)

    def request_delete(self, url):
        return self.request("delete", url, data=None)

    def request(self, method, url, data=None, params=None):
        self.set_headers()
        fn = getattr(requests, method)

        if not url.startswith("http"):
            url = urljoin(self.base_url, url)
        
        if data:
            if self.headers.get('Content-type', '').endswith("/json"):
                try:
                    data = json.dumps(data)
                except:
                    pass
            resp = fn(url, data=data, headers=self.headers, proxies=self.proxies)
        else:
            resp = fn(url, headers=self.headers, proxies=self.proxies)

        resp.status = resp.status_code
        return resp, resp.content


try:
    from quartus.cloud import CloudBaseConnection as Base
except ImportError:
    Base = RequestsBase


class AlteraApiConnection(Base):
    def __init__(self, base_url, token=None, proxy=None):
        super(AlteraApiConnection, self).__init__()
        self.token =  token
        self.proxies = None
        self.base_url = base_url
        self.set_proxy(proxy)

    def login(self, username, password, resource="/api-token-auth/login/"):
        self.set_headers()
        form = {
            'username': username,
            'password': password,
        }

        url = resource
        try:
            resp, content = self.request_post(url, form)
        except socket.error as e:
            raise ConnectionError("could not connect to server: " + str(e), url=url)

        if resp.status == 200:
            try:
                data = json.loads(content.decode())
            except json.JSONDecodeError as e:
                print(content.decode())
                print(str(e))
                return False
            self.token = data.get('token')
            if self.token:
                return True
        else:
            print(content.decode())
        return False   

    def set_headers(self):
        self.headers = {}
        self.headers["Accept"] = "application/json"
        self.headers["Content-type"] = "application/json"
        self.headers["X-Requested-With"] = "XMLHttpRequest"
        if self.token:
            self.headers["Authorization"] = "Token " + self.token
        self.headers["Referer"] = self.base_url

