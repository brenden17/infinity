#!/bin/bash  

#http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html

cd ~/workspace/infinity/
source ~/workspace/infinity/dist/bin/activate
cd ~/workspace/infinity/infinity/bigdata
ipython notebook --pylab inline
