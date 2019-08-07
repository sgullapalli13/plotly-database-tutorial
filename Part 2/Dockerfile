FROM python:3
LABEL maintainer="sgullapalli13@github.com"
WORKDIR /github_demo
COPY ./github_demo/requirements.txt /github_demo/requirements.txt
RUN pip install -r requirements.txt
COPY . /github_demo/ /github_demo/
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app.py"]
