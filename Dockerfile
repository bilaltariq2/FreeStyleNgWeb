# Use the official Nginx image as the base image
FROM nginx:latest

# Copy the HTML file to the Nginx document root
COPY index.html /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]
