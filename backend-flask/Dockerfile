FROM python:3.10-slim-buster

# Setting the working directory inside the container to /backend-flask
# All subsequent commands will be executed relative to this directory
# Make a new folder called /backend-flask inside the container
WORKDIR /backend-flask

# Copying requirements.txt file from the "outside(our dev env)"" to "inside the container"
COPY requirements.txt requirements.txt

# installing the requirements inside the container
RUN pip3 install -r requirements.txt

# Copying all the files and directories from the current directory on the host machine to
# the working directory (/backend-flask) inside the container.
COPY . .

# Setting environment variables (env vars)
# This is typically used to configure Flask to run in development mode
# which provides more detailed error messages and enables debugging features.
ENV FLASK_ENV=development

# Setting the port that our container will be listening on at runtime
# EXPOSE 4567
EXPOSE ${PORT}

# Command to run our Flask APP
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
