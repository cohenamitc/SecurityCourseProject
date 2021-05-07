from app import app
import os

if __name__ == '__main__':
    if int(os.environ.get('FLASK_SELF_SIGNED_CERT', 0)) == 1:
        app.run(host='0.0.0.0', ssl_context=('certs/server.crt', 'certs/server.key'))
    else:
        app.run(host='0.0.0.0')
