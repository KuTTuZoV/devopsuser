import os
from lib import create_app

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 8080))

def main():
    web, app = create_app()
    web.run_app(app, host=HOST, port=PORT)

if __name__ == '__main__':
    main()
