# Virtual-Computer-Science-Lab
Virtual Computer Science Lab is a utility to create a set of virtual machines on Digital Ocean that can be used by members of a classroom or organization.

Please note that at this time, this is just a proof of concept. The only utility provided is a script to create the VMs and SSH keys. All deletions will need to be done manually through your own provided scripts, or through the Digital Ocean management interface. If you want to change regions or images, you'll have to edit the hardcoded values in the script (this will be configurable some day, I promis).

## Getting Started
Install python-digitalocean, then clone this repo. I've cloned the project into a folder with a short name, just for the sake of this example
```
user:~/ $ pip install python-digitalocean
user:~/ $ git clone https://github.com/bplower/Virtual-Computer-Science-Lab.git vcsl
user:~/ $ cd vcsl
user:~/vcsl $ 
```

Now make a new Digital Ocean API key (You can do that [here!](https://cloud.digitalocean.com/settings/api/tokens)). This file will be automatically read when you run the deploy script.
```
user:~/vcsl $ echo "YOUR API KEY GOES HERE" > digital_ocean_api_token
user:~/vcsl $ 
```

Make a public keys directory, or change the hard coded value to an existing directory. If you don't already have your students public keys, get them from them somehow and save them in this directory. In this example, I'm just making brand new keys for our studends Jack and Jill.
```
user:~/vcsl $ mkdir pub_keys
user:~/vcsl $ cd pub_keys
user:~/vcsl/pub_keys $ ssh-keygen -t rsa -b 4096 -f jack -P ""
user:~/vcsl/pub_keys $ ssh-keygen -t rsa -b 4096 -f jill -P ""
user:~/vcsl/pub_keys $ cd ../
user:~/vcsl $
```

Make sure the script is adding Jack and Jill to the lab. These arguments are 
* Student Name (not actually used anywhere at the moment...)
* Username (used for somethings but I don't remember what exactly)
* SSH Public Key Path (where pubKeyDir is set to "pub_keys" by default)
```
lab.students.append(Student("Jack", "jack", pubKeyDir + "/jack.pub"))
lab.students.append(Student("Jill", "jill", pubKeyDir + "/jill.pub"))
```

Now run the script
```
user:~/vcsl $ ./deploy
Creating key:  student-jack
Creating key:  student-jill
Creating droplet: lab-jack
Creating droplet: lab-jill
user:~/vcsl $
```

On the Settings > Security page, you will see that two new keys have been added.
<img src="http://i.imgur.com/6UD27Lw.png" alt="Jack and Jills SSH keys in Digital Ocean">

And on the droplets page, you will see that two new droplets have been created. Each droplet only has the key for the designated student, so that students don't have access to each others VMs. All you have to do now is tell each student what IP their box is at, and then they can SSH in.
<img src="http://i.imgur.com/eyREyES.png" alt="Jack and Jills Droplets in Digital Ocean">
