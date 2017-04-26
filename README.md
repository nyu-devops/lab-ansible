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

### Ping for testing connectivity

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

### Ad-hock commands

To run a command on all servers use `all` as the target and `-a` followed by the command that you want to run:

    ansible all -a 'sudo apt-get update -y'

## Using Playbooks

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

### Using Dry Run mode

You can also run the playbooks in _Dry Run_ mode to check what would be changing if you atually ran it. You would use the `--check` flag to do this:

    ansible-playbook playbook.yaml --check

### Running a playbook

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

### Tips for debugging

The `debugging.yaml` file shows how to register variables during your run that contain information that is useful in debugging.

    ansible-playbook debugging.yaml

Produces the following output:
```
PLAY [webservers] *************************************************************

GATHERING FACTS ***************************************************************
ok: [web1]

TASK: [Show how to register output] *******************************************
changed: [web1]

TASK: [Show what was saved is JSON] *******************************************
ok: [web1] => {
    "output_from_pwd": {
        "changed": true,
        "cmd": "pwd ",
        "delta": "0:00:00.001082",
        "end": "2017-04-26 14:02:43.714501",
        "invocation": {
            "module_args": "pwd",
            "module_name": "shell"
        },
        "rc": 0,
        "start": "2017-04-26 14:02:43.713419",
        "stderr": "",
        "stdout": "/home/vagrant",
        "stdout_lines": [
            "/home/vagrant"
        ]
    }
}

TASK: [Get return code from JSON output] **************************************
ok: [web1] => {
    "msg": "Return code was 0"
}

PLAY RECAP ********************************************************************
web1                       : ok=4    changed=1    unreachable=0    failed=0
```

## Vagrant and Ansible

You can actually use Ansible to provision your Vagrant vm. The only prerequsite is that you have to already have Ansible installed on your laptop. The easiest way to do this for Python developers is with `pip install ansible`. There is an example at the bottom of the `Vagrantfile` that is commented out. It looks like this:
```
client.vm.provision "ansible" do |ansible|
  ansible.playbook = "python.yaml"
end
```
This will use the `python.yaml` included in this repo to provision your vm just like we have done with previous projects using the `shell` provisioner. The difference is thaty it will use Ansible and be idempotent so that it doesn't try and install things that are already installed like `shell` provisioning will.

## Experiment

You now have a small multi-server environment on your laptop where you can feel free to explore  more `ansible` commands that you've learned in class.
