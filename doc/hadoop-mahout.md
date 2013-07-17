# Hadoop and Mahout on Ubutu12.04

* install

~~~
$ wget http://archive.cloudera.com/cdh4/one-click-install/precise/amd64/cdh4-repository_1.0_all.deb
$ sudo dpkg -i cdh4-repository_1.0_all.deb
$ curl -s http://archive.cloudera.com/cdh4/ubuntu/precise/amd64/cdh/archive.key | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get install openjdk-7-jre openjdk-7-jdk mahout hadoop-conf-pseudo
~~~

set JAVA_HOME in /etc/hadoop/conf/hadoop-env.sh

~~~
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
~~~
