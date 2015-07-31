## Buildbot

### Souce clone
* git clone https://github.com/buildbot/buildbot.git
* cd buildbot
* git checkout v0.8.12 -b v0.8.12

### Install 
* Install master and slave

### Create master and slave
* buildbot create-master master
* buildslave create-slave slave localhost:9989 example-slave pass

### Links
* http://docs.buildbot.net/current/tutorial/firstrun.html
