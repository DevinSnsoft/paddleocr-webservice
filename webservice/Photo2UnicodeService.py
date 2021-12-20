#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
preference:
    http://spyne.io/docs/2.10/index.html
    https://github.com/arskom/spyne/blob/master/examples/helloworld_soap.py

This is a simple HelloWorld example to show the basics of writing
a webservice using spyne, starting a server, and creating a service
client.
Here's how to call it using suds:

#>>> from suds.client import Client
#>>> hello_client = Client('http://localhost:8000/?wsdl')
#>>> hello_client.service.say_hello('punk', 5)
(stringArray){
   string[] =
      "Hello, punk",
      "Hello, punk",
      "Hello, punk",
      "Hello, punk",
      "Hello, punk",
 }
#>>>

"""
# Application is the glue between one or more service definitions, interface and protocol choices.
import base64

from spyne import Application, String, srpc
# @rpc decorator exposes methods as remote procedure calls
# and declares the data types it accepts and returns
from spyne import rpc
# spyne.service.ServiceBase is the base class for all service definitions.
from spyne import ServiceBase
# The names of the needed types for implementing this service should be self-explanatory.
from spyne import Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
# Our server is going to use HTTP as transport, It’s going to wrap the Application instance.
from spyne.server.wsgi import WsgiApplication


# step1: Defining a Spyne Service
#from paddleocr import parse_args, parse_lang, get_model_config, BASE_DIR, VERSION, SUPPORT_DET_MODEL, SUPPORT_REC_MODEL


class Photo2UnicodeService(ServiceBase):
    # @rpc(Unicode, _returns=Iterable(Unicode))
    @srpc(String, _returns=String)
    def photo2unicode(imgstr):
        """Docstrings for service methods appear as documentation in the wsdl.
        <b>What fun!</b>
        @param name: the name to say hello to
        @param times: the number of times to say hello
        @return  When returning an iterable, you can use any type of python iterable. Here, we chose to use generators.
        """
        print(imgstr)
        filepath = '/home/tesla4/wjj/PaddleOCR-release-2.3/imgs/result.png'
        file_str = open(filepath, 'wb')
        file_str.write(base64.b64decode(imgstr))

        file_str.close()
        import os
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        import sys

        __dir__ = os.path.dirname(__file__)
        sys.path.append(os.path.join(__dir__, ''))

        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # need to run only once to download and load model into memory
        img_path = filepath
        img_path = img_path.replace('\\', '/')
        print("imag_path:", img_path)
        result = ocr.ocr(img_path, cls=True)
#        print(result)
#        if result == None:
#            return "don't recognized!"

        for line in result:
            print(line)
        temp_accuary = line[1][1]

        txts = [line[1][0] for line in result]

        f = open("result.txt", "w", encoding='utf-8')
        for i in txts:
            f.write(i)
        f.close()

        import codecs
        import json

        f2 = codecs.open("result.txt", "r", 'utf-8')
        listimg = []
        for i in range(1):
            lines = f2.read(1)
            listimg.append(lines)
        print(len(listimg))
        dict = {'gbk': listimg}
        jStr = json.dumps(dict)
        print(jStr)

        jStr = jStr.encode()
        with open('result.json', 'wb')as f:
            f.write(jStr)

        result_unicode = json.dumps(listimg[-1]).replace('"', '')

        return result_unicode

    @srpc(String, _returns=String)
    def findunicode(zistr):
        f = open("result.txt", "w", encoding='utf-8')
        for i in zistr:
            f.write(i)
        f.close()

        import codecs
        import json

        f2 = codecs.open("result.txt", "r", 'utf-8')
        listimg = []
        for i in range(1):
            lines = f2.read(1)
            listimg.append(lines)
        print(len(listimg))
        dict = {'gbk': listimg}
        jStr = json.dumps(dict)
        print(jStr)

        jStr = jStr.encode()
        with open('result.json', 'wb')as f:
            f.write(jStr)

        result_unicode = json.dumps(listimg[-1]).replace('"', '')
        return result_unicode



# step2: Glue the service definition, input and output protocols
soap_app = Application([Photo2UnicodeService], 'spyne.examples.hello.soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

# step3: Wrap the Spyne application with its wsgi wrapper
wsgi_app = WsgiApplication(soap_app)

if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    # configure the python logger to show debugging output
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    # step4:Deploying the service using Soap via Wsgi
    # register the WSGI application as the handler to the wsgi server, and run the http server
    server = make_server('210.30.0.92', 8000, wsgi_app)
    server.serve_forever()
