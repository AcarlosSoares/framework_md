from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#     host = os.getenv('IP', '0.0.0.0')
#     port = int(os.getenv('PORT', 5000))
#     app.debug = True
#     app.run (host=host, port=port)
