#FROM ansible/ubuntu14.04-ansible:latest
FROM python:3.7
RUN mkdir -p \
    /opt/mqtttossh/playbook \
    /usr/src/app
COPY . /usr/src/app/
WORKDIR /usr/src/app
COPY ./playbook/fact.yml /opt/mqtttossh/playbook/fact.yml
COPY ./playbook/inventory.yml.dist /opt/mqtttossh/inventory.yml
COPY ./main.conf.dist /opt/mqtttossh/main.conf
RUN apt-get update && \
    apt-get install -y ansible && \
    rm -rf /var/lib/apt/lists/*
RUN make install
ENTRYPOINT ["python", "-u", "main.py"]
