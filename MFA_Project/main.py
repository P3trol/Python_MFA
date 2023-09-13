from website import create_app # Import create app function

app = create_app() # Create app

if __name__ == '__main__': # Check if main
    app.run(debug=True) # Run app