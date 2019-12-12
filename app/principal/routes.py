from flask import render_template, Blueprint
import os

principal = Blueprint('principal', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@principal.route('/')
@principal.route('/home', methods=['GET'])
def inicio():
    return render_template('principal.html', title='home')


@principal.route('/sobre', methods=['GET'])
def sobre():
    return render_template('about.html', title='sobre')
