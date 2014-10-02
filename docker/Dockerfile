# http://phusion.github.io/baseimage-docker/
# https://registry.hub.docker.com/_/jenkins/
FROM phusion/baseimage

USER root
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Java
# https://github.com/dockerfile/java/blob/master/oracle-java8/Dockerfile

RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer

ENV JAVA_HOME /usr/lib/jvm/java-8-oracle


# Common tools
RUN sudo apt-get install -y build-essential git


# Python

RUN apt-add-repository -y ppa:fkrull/deadsnakes
RUN apt-get update

RUN apt-get install -y python2.6 python2.6-dev \
    python2.7 python2.7-dev python3.3 python3.3-dev \
    python3.4 python3.4-dev python-virtualenv python-tox


# Sqlite

RUN apt-get install sqlite3


# PostgeSQL
# https://github.com/vpicavet/docker-pggis/blob/master/Dockerfile
# https://github.com/sameersbn/docker-postgresql/blob/master/start

RUN apt-get install -y postgresql-common &&
    echo "create_main_cluster = false" >> /etc/postgresql-common/createcluster.conf  && \
    apt-get install -y postgresql-9.3 postgresql-client-9.3 libpq-dev python-psycopg2 python3-psycopg2  && \
    echo "postgres" > /var/lib/postgresql/pwfile
    sudo -u postgres -H /usr/lib/postgresql/9.3/bin/initdb --pwfile=/var/lib/postgresql/pwfile --pgdata=/var/lib/postgresql/9.3/main/ --username=postgres --encoding=unicode --auth=trust
    # https://github.com/orchardup/docker-postgresql/blob/master/run

#RUN mkdir /etc/service/postgresql
#ADD data/postgresql.sh /etc/service/postgresql/run

#RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
#RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

#ADD data/pgpass /root/.pgpass
#RUN chmod 700 /root/.pgpass

#EXPOSE 5432
# VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# MySQL
# https://github.com/fideloper/docker-mysql/blob/master/Dockerfile

#RUN echo "mysql-server mysql-server/root_password password root" | debconf-set-selections && \
#    echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections && \
#    apt-get install -y mysql-server python-mysqldb

#RUN mkdir /etc/service/mysql
#ADD data/mysql.sh /etc/service/mysql/run

#EXPOSE 3306


# External tools
#RUN apt-get install -y sloccount npm
#RUN npm install -g csslint jshint


# Jenkins
# https://github.com/cloudbees/jenkins-ci.org-docker/blob/master/Dockerfile

# RUN \
#  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 150FDE3F7787E7D11EF4E12A9B7D32F2D50582E6 && \
#  echo deb http://pkg.jenkins-ci.org/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list && \
#  apt-get update && apt-get install -y jenkins

#VOLUME /var/lib/jenkins

# EXPOSE 8080
# EXPOSE 50000

# RUN mkdir /etc/service/jenkins
# ADD data/jenkins.sh /etc/service/jenkins/run

#USER jenkins

#RUN wget https://127.0.0.1:8080/jnlpJars/jenkins-cli.jar -o $JENKINS_HOME/jenkins-cli.jar
#RUN java -jar $JENKINS_HOME/jenkins-cli.jar install-plugin cobertura violation sloccount xvfb


# Finalizing  baseimage-docker's
#CMD ["/sbin/my_init"]
#RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*