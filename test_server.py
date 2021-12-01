import http.server
import socketserver
import json
import datetime


def cumulative_interest_rate(args):
    """Cumulative interest rate.

    Args:
        param1 (dictionary): Arguments. e.g. {
            'sum': 360000, 'rate': 12.5, 'date1': '01.02.2019', 'date2': '05.06.2025', simple:True
            }

    Returns:
        float: The return value. -1 if error, positive number otherwise.

    """
    res = -1  # Returns -1 if something wrong
    try:
        date1 = datetime.datetime.strptime(args['date1'], '%d.%m.%Y')
        date2 = datetime.datetime.strptime(args['date2'], '%d.%m.%Y')
        sum = args['sum']
        rate = args['rate']
        if date2 > date1 and rate > 0 and sum > 0:
            period = (date2 - date1).days
            rate = rate/(100*365)  # percent per day
            if args['simple']:  # Простые проценты
                res = (period * rate) * sum
            else:  # Проценты на сумму займа плюс накопленные проценты
                res = 0
                for day in range(period):
                    res += (sum + res)*rate
    except:
        return -1

    return res


# Server logic

PORT = 8000


class MyHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        # request

        content_length = int(self.headers['Content-Length'])

        if content_length:
            input_json = self.rfile.read(content_length)
            try:  # if we received bad 'json'
                input_data = json.loads(input_json)
            except:
                input_data = None
        else:
            input_data = None

        print(input_data)

        # response
        response = None

        if input_data:
            response = {'status': 'OK',
                        'result': cumulative_interest_rate(input_data)}
        else:
            response = {'status': 'ERROR', 'result': 'Bad request format'}

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        output_json = json.dumps(response)

        self.wfile.write(output_json.encode('utf-8'))


# Run server

Handler = MyHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Starting http://localhost:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("Stopping by Ctrl+C")
    # to resolve problem `OSError: [Errno 98] Address already in use
    httpd.server_close()
