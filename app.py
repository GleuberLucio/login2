from app_login import init_app

app = init_app()

if __name__ == '__main__':
    app.run(debug=True, port=8000)