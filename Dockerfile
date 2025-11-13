# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
 

# Make port 8080 available to the world outside this container (if applicable)
EXPOSE $PORT

# Define the command to run your application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT


# sudo groupadd docker 2>/dev/null || true
# sudo usermod -aG docker "$USER"
# docker login 
# heroky login 
# heroku container:login
# sudo docker buildx build .  -t registry.heroku.com/metasploit-gui/web  --provenance=false --push 
# sudo heroku container:release web -a metasploit-gui 
# sudo heroku logs --tail 
