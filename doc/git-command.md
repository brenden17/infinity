# Git command

## basic command
from [here](http://rogerdudler.github.io/git-guide/index.ko.html)
~~~
git init
git clone /local/repository/path
git clone usename@host:remote/repository/path
git add filename
git commit -m "comment"
git push origin master
git checkout -- filename #revert
git checkout -b features #new branch
git checkout -d features #delete branch
git checkout master #merge branch
git pull
git log
git tag 1.0.0 indicator
~~~

## git repository 
Create a new repository on the command line
~~~
touch README.md 
git init 
git add README.md 
git commit -m "first commit" 
git remote add origin https://github.com/brenden17/docs.git 
git push -u origin master
~~~

Push an existing repository from the command line
~~~
git remote add origin https://github.com/brenden17/docs.git git push -u origin master
~~~
