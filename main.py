from website import create_app
app = create_app()

if __name__ == '__main__': # only run the web server when we actually run the main
    app.run(debug = True) # update each time changing the code (hot update)