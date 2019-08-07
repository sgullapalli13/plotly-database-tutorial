# plotly-database-tutorial: Part 3
 

Now that we have a web app to show our data, we want everyone to be able to see it. Using Google’s Cloud Platform, we can host the site and access it from anywhere. 

We can start by making a Google Cloud account. After setting that up, go to Compute Engine, then look at your VM instances. Hit Create Instance, and choose a Linux or Ubuntu system (I used Ubuntu 19.03). Allow http and https, then save the VM. Note the button to SSH into the VM that will open a terminal to access your VM from.

Before we can dockerize our code, we need to add a Dockerfile in our project folder. It has to be at the highest level of your project to copy the files it needs.
```
FROM python:3
LABEL maintainer=”sgullapalli13@github.com”
WORKDIR /github_demo
COPY ./requirements.txt /github_demo/requirements.txt
RUN pip install -r requirements.txt
COPY . /github_demo/
EXPOSE 8080
ENTRYPOINT [“python”]
CMD [“app.py”]
```

We want to build this on a python image so we don’t have to install python. We copy all our files into the container then run requirements so it installs all our dependencies. Flask defaults output to port 5000, but I specified in my app that I’d like to output on 8080, so we expose that. Finally, we have the command to run our program.

Note: I am choosing to dockerize the code within the VM, but it is possible to dockerize locally and send the image to the VM to run it there. 

Save the project and push it to Github or find some way to transfer it into the VM. SSH into the VM and clone your code, and cd into your project folder. Install docker on the VM if it’s not already installed, and run ```sudo docker run hello-world``` to make sure it’s working correctly. 

Now we are going to build the image and container.
```sudo docker build -t <container>:latest .```
And run the container with
```sudo docker run --name <container name> -p 80:8080 -d <container>```

Here we are giving the container a name so we can more easily refer to it later on. Also, -p maps the external port we can view it at to the internal port. HTTP protocols run on port 80. 

We can use ```sudo docker ps``` to view our running container. 

Our app is up and running now! To see it on the internet, we can go back to the Google Cloud page and find the IP address of the VM. Paste this into your browser followed by the port. It should look something like this: 

Note: If your app is not showing up, first make sure your code isn’t throwing errors with ```sudo docker logs --tail 100 <container name>``` to see what was sent to the console logs. Then check to make sure your IP mapping is correct.

That’s the end of this tutorial! Now you know how to build and deploy a web app using plotly, flask, and docker.

