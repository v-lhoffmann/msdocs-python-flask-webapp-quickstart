import os
import random
import math
import cProfile
import pstats
import io
from pstats import SortKey

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


def square():
    i = 1
    ans = 0
    while i < 1000000:
        ans = math.sqrt(i)
        i = i + 1


def bigmem():
    bigarray = []
    i = 1
    while i < 1000000:
        bigarray.append(random.randint(1, 100000000))
        i = i + 1


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        if name == "square":
            pr = cProfile.Profile()
            pr.enable()
            square()
            pr.disable()
            s = io.StringIO()
            sortby = SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.dump_stats('square.txt')
            ps.print_stats()
            print(s.getvalue())
        elif name == "bigmem":
            pr = cProfile.Profile()
            pr.enable()
            bigmem()
            pr.disable()
            s = io.StringIO()
            sortby = SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.dump_stats('bigmem.txt')
            ps.print_stats()
            print(s.getvalue())
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
