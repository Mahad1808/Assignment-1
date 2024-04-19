FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application
COPY . .

EXPOSE 5000

ENV NAME World

# Command to run the Flask server
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


#docker build -t my-flask-app .