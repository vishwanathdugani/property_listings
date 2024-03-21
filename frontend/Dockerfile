# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in package.json
RUN npm install
RUN npm install vue-slider-component


# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run npm run serve when the container launches
# CMD ["npm", "run", "serve"]
