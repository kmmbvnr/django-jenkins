#!/bin/bash

/usr/bin/java -Djava.awt.headless=true \
              -jar /usr/share/jenkins/jenkins.war \
              --webroot=/var/cache/jenkins/war \
              --httpPort=8080 --ajp13Port=-1
