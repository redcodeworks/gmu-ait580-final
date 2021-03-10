# gmu-ait580-final

## Deployment

There a several options for running this project. This app was designed to read data from a private S3 bucket using AWS credentials, which are definied as environment variables. However, this branch of the project has the URL hardcoded to a public bucket to simplify setup for grading purposes.


### Docker Compose

Docker Compose defines the stack of services to deploy in a YAML file. Docker compose is included with docker desktop on macOS and Windows. Linux distributions need to have this installed seperately.

1. Ensure Docker is installed and running.
2. From the terminal, change to the root project directory this this readme file is in, and simply run:

        docker compose up

3. **Ignore the terminal output as the url is incorrect!** Once the container is running, navigate to [http://127.0.0.1:8501].


### Dockerfile

If docker compose is not an option, you can build the image yourself and run the container. 

1. From the terminal, change to the directory this this readme file is in, and run:

        docker build -f Dockerfile -t gmu-ait580-final:latest .

2. Then run the container directly.

        docker run --name gmu-ait580-final -p 8501:8501 gmu-ait580-final:latest 

3. **Ignore the terminal output as the url is incorrect!** Once the container is running, navigate to [http://127.0.0.1:8501].


### Python

Alternatively, you can setup the server yourself. 

1. From the terminal, setup a new virtualenv and activate it.
2. Change directory to this readme file.
3. Install the package dependencies located in requirements.txt.
   
        pip install -r requirements.txt

4. Change directory to the project folder, gmu-ait580-final. The python scripts and data_cleaning json are located here.
5. Run the following command:
   
        streamlit run app.py

6.  Once the container is running, navigate to [http://127.0.0.1:8501].