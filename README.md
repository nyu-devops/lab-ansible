# lab-ansible
This repository is part of lab for the *NYU DevOps* class for Spring 2017, [CSCI-GA.3033-013](http://cs.nyu.edu/courses/spring17/CSCI-GA.3033-013/) on using Ansible for Configuration Management.

This lab demonstrates how to use Ansible to create and configure Virtual Machines

## Setup

For easy setup, you need to have [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) installed. Then all you have to do is clone this repo and invoke vagrant:

    git clone https://github.com/nyu-devops/lab-ansible.git
    cd lab-ansible
    vagrant up
    vagrant ssh client
    cd /vagrant

You can now run `ansible` commands.

## Manually running Ansible

The `Vagrantfile` in this repo will create three (3) virtual machines: client, web, & db. Each contains 256MB of memory so all together they will take up 768MB of memory on your laptop while running.

To see if everything is working you can `vagrant ssh client` and issue the command:

    cd /vagrant
    ansible -m ping all

It should respond with:
```
    web1 | success >> {
        "changed": false,
        "ping": "pong"
    }

    db1 | success >> {
        "changed": false,
        "ping": "pong"
    }
```

To run the playbook use:

    ansible-playbook playbook.yaml

This will execute the commands that are in `playbook.yaml` and display quite a lot of output on the console as it executes. Feel free to explore with more `ansible` commands that you've learned in class.
