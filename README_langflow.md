# Langflow

This folder contains the configuration for Langflow, a tool that allows you to use language models in your applications.

## Project Structure

- `Dockerfile` : Configuration file to build the Docker image for Langflow.
- `requirements.txt` : List of dependencies required to run Langflow.

## Running with Docker

1. **Build the Docker Image**

   *Open a terminal in the `langflow` folder and run the following command to build the image:*
   docker build -t langflow .

2. **Start the Docker Container**  
`docker run -p 7860:7860 langflow`

- [Langflow sera accessible à l'adresse]( http://127.0.0.1:7860/).
- [Telecharger langflow test ibl_education.json via ce lien drive:](https://drive.google.com/file/d/1NpcS7FlK803Xordb0toB46VshnNYTIwO/view?)usp=drive_link

3. **Model Details**
Model ID : `EleutherAI/gpt-neo-2.7B`
API Token: Use the following Hugging Face API key: `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`

4. **Configuration in the Code**
Open the API code in Flow and modify the flow_id and necessary tweaks in consumers1.py to get Langflow working with your Django application.
For example:
flow_id: aa2ba4f0-2573-4e52-aba8-117ca1bc019a
TWEAKS = {
              "Prompt-B5He1": {},
              "ChatOutput-9Tl1t": {},
              "HuggingFaceModel-pmzcj": {},
              "ChatInput-RdX5F": {}
        }
