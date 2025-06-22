FROM python:3.11-slim

# Create non-root user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# Create working directory and set up environment
WORKDIR /home/appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
#COPY app.py .
COPY flaskapp.py .
COPY configuration/ configuration/

# Create /var/dbfile as root, give permissions to appuser
RUN mkdir -p /var/dbfile && chown appuser:appgroup /var/dbfile && chmod 775 /var/dbfile

# Switch to non-root user
USER appuser

# Configure the Flask application to listen on port 5000
EXPOSE 5000

# flaskapp:app --> flaskapp.py:app object
# Each Gunicorn worker is a separate process with seperate mem-space, so app will be initialized 4 times by 4 worker-process
CMD ["gunicorn", "app:fapp", "-w", "4", "-b", "0.0.0.0:5000", "--log-level=debug","--reload"] 


# ########### DOCKER command to follow #################### :

#  sudo docker build -t my_flask_app .
#  sudo docker run -it -p 5000:5000 my_flask_app   
#  sudo docker compose up
#  Standalone flask code : flask --app flaskapp run
#  stand-alone Flask app with ENV file passed : docker run --env-file configuration/sample.env -it -p 5000:5000 my_flask_app

## -- Docker-compose --
# sudo docker compose up

## CURL 
# curl -H "X-API-KEY: abcdef12345" http://localhost:5000/users?api_key=abcdef12345
# curl -H "X-API-KEY: abcdef12345" http://localhost:5000/system?api_key=abcdef12345

# pytest : pytest -c configuration/pytest.ini
# pytest --html=reports/report.html --self-contained-html


