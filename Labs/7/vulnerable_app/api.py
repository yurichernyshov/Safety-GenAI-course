"""
API модуль с уязвимостями
"""

import os
import subprocess
import pickle
import base64
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping_host():
    """Уязвимость: Command Injection"""
    host = request.args.get('host', 'localhost')
    
    # ОПАСНО: Выполнение системной команды с пользовательским вводом
    os.system(f"ping -c 4 {host}")
    return "Ping completed"

@app.route('/execute')
def execute_command():
    """Уязвимость: Command Injection (subprocess)"""
    cmd = request.args.get('cmd', 'ls')
    
    # ОПАСНО: shell=True с пользовательским вводом
    subprocess.run(cmd, shell=True)
    return "Command executed"

@app.route('/deserialize')
def deserialize_data():
    """Уязвимость: Insecure Deserialization"""
    data = request.args.get('data', '')
    
    # ОПАСНО: Десериализация ненадёжных данных
    obj = pickle.loads(base64.b64decode(data))
    return str(obj)

@app.route('/eval')
def evaluate_code():
    """Уязвимость: Code Injection"""
    code = request.args.get('code', '')
    
    # ОПАСНО: Выполнение произвольного кода
    result = eval(code)
    return str(result)

if __name__ == '__main__':
    # Уязвимость: Debug mode in production
    app.run(debug=True, host='0.0.0.0')
