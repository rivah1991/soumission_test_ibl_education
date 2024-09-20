# Backend Django

This folder contains the backend application developed with Django, which exposes a REST API

## Project Structure

- `base/` :  Directory containing the Django API.
- `manage.py` : Script for managing Django commands.
- `requirements.txt` : List of Python dependencies required for the application.
- `Dockerfile` : File for creating the Docker image of the application.


## Installation and Execution

1. **Create the Docker Image**

   *Navigate to the backend_django folder and run the following command to build the Docker image:* 
   docker build -t django-rest-app .

   *Once the image is created, you can run the container with the following command:*
   docker run -d -p 8000:8000 django-rest-app

## Creating a Superuser

To access the Django admin interface, you first need to create a superuser. Follow the steps below:

1. Open the terminal where your Django project is running.

2. *Run the following command:*
   python manage.py createsuperuser

3. *Open a terminal and execute the following command to create a superuser in the running container:*
   docker exec -it <container_name_or_id> python manage.py createsuperuser