#!/usr/bin/python
# Author: Brahm Lower
# Requirements:
#   python-digitalocean
# Description:
#   This is a script to deploy a virtual computer science lab, which can be used
#   to provide students with a VM for use in a computer science lecture or lab.

import digitalocean

class Lab(object):
    def __init__(self, name):
        self.name = name
        self.computers = []
        self.students = []
        self.extraKeys = []

    def addComputer(self, computer):
        for i in self.extraKeys:
            computer.ssh_keys.append(i.public_key)
        self.computers.append(computer)
    
    def deploy(self):
        for student in self.students:
            self.deployToStudent(student)
    
    def deployToStudent(self, student):
        # Get list of current droplets
        currentDroplets = []
        for i in digitalocean.Manager(token = doApiToken).get_all_droplets():
            currentDroplets.append(i.name)
        # Start deploying droplets to students
        for computer in self.computers:
            # If the droplet doesn't already exist
            if computer.baseName % student.username not in currentDroplets:
                computer.deployToStudent(student, quiet = False)
            else:
                print "Droplet exists: %s" % (computer.baseName % student.username)

class Student(object):
    def __init__(self, name, username, sshKeyFile):
        self.name = name
        self.username = username
        self.sshKey = loadKey("student-" + self.username, sshKeyFile)

class Computer(digitalocean.Droplet):
    # This extends the base Droplet class, which means we don't have to deal
    # with the name and region and everything
    def __init__(self, baseName, region, image, slug):
        super(Computer, self).__init__(token = doApiToken, region = region, image = image, size_slug = slug)
        self.baseName = baseName
        self.ssh_keys = []
    
    def deployToStudent(self, student, quiet = True):
        # Prepare the VM information
        self.name = self.baseName % student.username
        self.ssh_keys.append(student.sshKey.public_key)
        # Deploy the VM
        print "Creating droplet: %s" % self.name
        self.create()
        
def loadKey(keyName, keyFile):
    keyValue = open(keyFile).read().strip()
    sshKey = digitalocean.SSHKey(token = doApiToken)
    sshKey.load_by_pub_key(keyValue)
    if not sshKey.fingerprint:
        print "Creating key: %s" % keyName
        sshKey = digitalocean.SSHKey(token = doApiToken, public_key = keyValue, name = keyName)
        sshKey.create()
    else:
        print "Key already exists: %s" % keyName
    return sshKey

doApiTokenFile = "digital_ocean_api_token"
doApiToken = open(doApiTokenFile).read()
pubKeyDir = "pub_keys"

if __name__ == "__main__":
    lab = Lab("Lecture 1")
    # Add keys for the lab
    #lab.extraKeys.append(loadKey("admin-key", pubKeyDir + "/admin-key.pub"))
    # Add computers to the lab
    lab.addComputer(Computer("lab-%s", "nyc2", "ubuntu-14-04-x64", "512mb"))
    # Add users to the lab
    lab.students.append(Student("Jack", "jack", pubKeyDir + "/jack.pub"))
    lab.students.append(Student("Jill", "jill", pubKeyDir + "/jill.pub"))
    # Deploy the lab
    lab.deploy()
