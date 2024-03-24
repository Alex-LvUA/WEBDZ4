from datetime import date
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
from pathlib import Path
import json
from datetime import datetime


class MyFramework(BaseHTTPRequestHandler):
    def do_POST(self):
        #print(f"{self.headers.get('Content-Length')=}")
        data = self.rfile.read(int(self.headers['Content-Length']))
        print( data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        #data_dict_time[str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))]=data_dict

        print(data_dict)
        try:
             with open('storage/data.json',  encoding='utf-8') as fh:
                data_file=json.load(fh)

        except FileNotFoundError:
            data_file=dict()
        data_file[str(datetime.now())] = data_dict

        with open('storage/data.json','w', encoding='utf-8') as fh:
            json.dump(data_file, fh)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()


    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        match pr_url.path:
            case '/' | '/index.html':
                self.send_html('index.html')
            case '/message.html':
                self.send_html('message.html')
            case _:
                file_path=Path(pr_url.path[1:])
                #print(f"{file_path.exists()=}")
                if file_path.exists():
                    self.send_stat(file_path)
                else:
                    self.send_html('error.html',404)

    def send_stat(self,filename_stat,code=200):
        self.send_response(code)
        mt=mimetypes.guess_type(self.path)
        self.send_header('Content-type', mt[0])
        self.end_headers()
        with open(filename_stat, 'rb') as fh:
            self.wfile.write(fh.read())
    def send_html(self,filename_html,code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename_html, 'rb') as fh:
            self.wfile.write(fh.read())





def run_server():
    address = ('localhost',8082)
    http_server=HTTPServer(address, MyFramework)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

if __name__ == '__main__':
    run_server()