https://github.com/DataRootUniversity/ds-fundamentals/blob/master/docker-flask-project/DOC.md#dockerize-your-app

Dockerize your app
In this section, we'll create our own Docker container for the created application. So, you'll need the following packages:

SQLAlchemy
Flask
Flask_SQLAlchemy
psycopg2
Create a folder app that will serve as a root for your project. Create requirements.txt file and put there names of packages from above

In the root of your project create a new text file and write the following commands:

FROM python:3.7

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/app'

COPY . .

CMD ["python", "./run.py"]
Upon doing this, build the Docker image with the following command in the root of your project: docker build -t <user-name>/<name-of-the-container>:<tag-name> .
and run it:
docker run --network=host --env DB_URL=postgresql+psycopg2://test_user:password@localhost/test_db -p 8000:8000 <user-name>/<name-of-the-container>:<tag-name>

Now your application is running in the docker container! You should test it the same way you did it earlier.

To submit the project, push the image to the Docker Hub using: docker push <user-name>/<name-of-the-container>:<tag-name>

Then provide its name to the @DRU Bot.

If you have any questions, write @DRU Team in Slack!