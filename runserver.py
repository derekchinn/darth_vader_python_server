from web import app, config

# Run the server
app.run(debug=config["server"]["DEBUG"],
		host=config["server"]["HOST_IP"])