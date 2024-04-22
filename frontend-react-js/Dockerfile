FROM node:16.18

ENV PORT=3000

# Copying all the files and directories from the current directory on the host machine to
# /frontend-react-js inside the container
# if /frontend-react-js does not exist in the container docker will
# create it for us
COPY . /frontend-react-js

# Specifying the workdir because we want all subsequent commands to run
# inside this working directory
WORKDIR /frontend-react-js

# Installing and Adding layers
RUN npm install

# Defining the port that our container will be listening on at runtime
EXPOSE ${PORT}

# Command to run our react APP
CMD ["npm", "start"]
