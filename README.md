## Prerequisites

Before you begin, make sure you have installed:

- [Docker](https://www.docker.com/get-started)


This project consists of several components, each with its own README for detailed instructions.

## Components

- [Django](README_django.md)
- [Flutter](README_flutter.md)
- [Langflow](README_langflow.md)
- [ReactJS](README_reactjs.md)



# Deploying Docker Swarm Services

This folder contains the configuration needed to deploy Docker Swarm services for your application.

## Configuration File

A docker-compose.yml file is present in the root directory. This file defines the services to be deployed for the different folders: backend_django, frontend_react, langflow, and mobile_django.

## Deploying Docker Swarm Services

To deploy the services, run the following command in the terminal from the directory containing the docker-compose.yml file:


*docker stack deploy -c docker-compose.yml chat_app*

To see the list of Docker networks, use the command:
*docker network ls*
If you have made changes to the image or configurations that are not yet taken into account, you can force the update of the Django service with the following command: 
*docker service update --force name_service*
Replace name_service with the name of your service.
To display the list of running Docker Swarm services, use the command:
*docker service ls*

## Testing the Django API with Open edX

This section describes how to test the Django API using Open edX

### Steps to Test the API

1. **Create a Section, Subsection, and Unit**

   - Go to Create Section in Open edX.
   - Then, go to Create Subsection.
   - Finally, click on Create Unit.

2. **Configure the Test in the Unit**

   - In the created unit, select the Text option.
   - Choose Raw HTML to insert custom content.

3. **Copy and Paste the HTML Code**

   - Copy the HTML code from the following file :       
     OpenEdx/openEdx_django_rest.html   
   - Paste it into the Raw HTML field in Open edX..

4. **Finalize and Test**

   - Save the changes and ensure that the unit correctly tests the Django API.
