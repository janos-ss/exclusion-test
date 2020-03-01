This directory is usefull for developers. You can define here routine to manipulate your code. Then, add the routine to the file in dev, and it will be call at each correspondant event (commit, prepush). See how its done in .githooks 

This way of functionning is language agnostic and you just have to change the script in /dev for each of your projects.

To activate thos hooks, go to .githooks and run the share script. 
