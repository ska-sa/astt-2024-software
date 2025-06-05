# This Dockerfile is used to build the frontend application using Node.js and Alpine Linux.
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./
# Install the application dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the application code to the working directory
COPY . .

# Build the application
RUN npm run build -- --prod --output-path=/www/localhost/htdocs

# Get apache2 package
RUN apk add --no-cache apache2

# Copy the built application to the Apache document root
RUN cp -r dist/* /var/www/localhost/htdocs/

# Expose port 80 for the Apache server
EXPOSE 80

# Start the Apache server in the foreground
CMD ["httpd", "-D", "FOREGROUND"]