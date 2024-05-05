from Flask.Website import create_app

app = create_app()

if __name__ == "__main__":
    # Run the Flask app on its own independent process
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)