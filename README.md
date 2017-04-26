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

## Running Ansible

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

To run a command on all servers use `all` as the target and `-a` followed by the command that you want to run:

    ansible all -a 'sudo apt-get update -y'

But the real power of Ansible is in it's playbooks. To see which tasks will be executed when running a playbook use the `--list-tasks` flag:

    ansible-playbook playbook.yaml --list-tasks

You should see output like the following:
```
playbook: playbook.yaml

  play #1 (all):
    Make sure all servers have the latest catalog
    Remove any unneeded packages
    Make sure all servers have the latest OS patches

  play #2 (webservers):
    Ensure that Apache is at the latest version
    Start Apache Services

  play #3 (dbservers):
    Ensure Redis is installed
    Start Redis

  play #4 (webservers:dbservers):
    Stop UFW NOW!!!
```
You can also run the playbooks in _Dry Run_ mode to check what would be changing if you atually ran it. You would use the `--check` flag to do this:

    ansible-playbook playbook.yaml --check

Finally to run the playbook change your servers use:

    ansible-playbook playbook.yaml

This will execute the commands that are in `playbook.yaml` and display output like the following:
```
PLAY [all] ********************************************************************

GATHERING FACTS ***************************************************************
ok: [web1]
ok: [db1]

TASK: [Make sure all servers have the latest catalog] *************************
changed: [db1]
changed: [web1]

TASK: [Remove any unneeded packages] ******************************************
changed: [db1]
changed: [web1]

TASK: [Make sure all servers have the latest OS patches] **********************
changed: [db1]
changed: [web1]

PLAY [webservers] *************************************************************

GATHERING FACTS ***************************************************************
ok: [web1]

TASK: [Ensure that Apache is at the latest version] ***************************
changed: [web1]

TASK: [Start Apache Services] *************************************************
ok: [web1]

NOTIFIED: [restart apache2] ***************************************************
changed: [web1]

PLAY [dbservers] **************************************************************

GATHERING FACTS ***************************************************************
ok: [db1]

TASK: [Ensure Redis is installed] *********************************************
changed: [db1]

TASK: [Start Redis] ***********************************************************
ok: [db1]

PLAY [webservers:dbservers] ***************************************************

GATHERING FACTS ***************************************************************
ok: [db1]
ok: [web1]

TASK: [Stop UFW NOW!!!] *******************************************************
changed: [db1]
changed: [web1]

PLAY RECAP ********************************************************************
db1                        : ok=9    changed=5    unreachable=0    failed=0
web1                       : ok=10   changed=6    unreachable=0    failed=0
```

You now have a small multi-server environment on your laptop where you can feel free to explore  more `ansible` commands that you've learned in class.
