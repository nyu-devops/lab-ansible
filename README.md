# lab-ansible
This repository is part of lab for the *NYU DevOps* class for Fall 2017, [CSCI-GA.3033-013](http://cs.nyu.edu/courses/fall17/CSCI-GA.3033-014/) on using Ansible for Configuration Management.

This lab demonstrates how to use Ansible to create and configure Virtual Machines. While the majority of this course uses Platform as a Service, there are times when you may need to setup your own infrastructure in-house and it's important that even that is full automated.

## Setup

For easy setup, you need to have [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) installed. Then all you have to do is clone this repo and invoke vagrant:

    git clone https://github.com/nyu-devops/lab-ansible.git
    cd lab-ansible
    vagrant up
    vagrant ssh client
    cd /vagrant

You can now run `ansible` commands.

## Running Ansible

The `Vagrantfile` in this repo will create three (3) virtual machines: client, web, & db. Each contains 256MB of memory so all together they will take up 768MB of memory on your laptop while running. The client machine is provided so that you don't have to install Ansible locally on your computer. The other two are a web server and database server which we will configure with Ansible from the client machine.

**Note:** _Because we have multiple vurtual machines, you cannot simply use the command `vagrant ssh` without specifying the VM that you want to `ssh` into so you always have to use `vagrant ssh client` to get to the client VM._

### Ping for testing connectivity

To see if everything is working you can `vagrant ssh client` and issue the command:

    cd /vagrant
    ansible -m ping all

It will respond with:
```
web1 | FAILED! => {
    "changed": false,
    "failed": true,
    "module_stderr": "",
    "module_stdout": "bash: /usr/bin/python: No such file or directory\r\n",
    "msg": "MODULE FAILURE",
    "parsed": false
}
db1 | FAILED! => {
    "changed": false,
    "failed": true,
    "module_stderr": "",
    "module_stdout": "bash: /usr/bin/python: No such file or directory\r\n",
    "msg": "MODULE FAILURE",
    "parsed": false
}
```

What happened? Ansible needs Python installed on all of the nodes in order to work. We can fix this with Ansible by making sure that Pythin is installed first. Do so this run the `prechecks.yaml` playbook like this:

    ansible-playbook prechecks.yaml

This will respond with:
```
PLAY [Ensure connectivity to all nodes] ****************************************

TASK [Check if python is installed] ********************************************
ok: [web1]
ok: [db1]

TASK [Install python] **********************************************************
ok: [web1]
ok: [db1]

TASK [Ensure that aptitude is installed] ***************************************
changed: [web1]
changed: [db1]

PLAY RECAP *********************************************************************
db1                        : ok=3    changed=1    unreachable=0    failed=0
web1                       : ok=3    changed=1    unreachable=0    failed=0
```

Now we can try and `ping` the nodes again with:
```
    ansible -m ping all
```

It should respond with:
```
db1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
web1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### Ad-hock commands

You can run ad-hock commands on servers if needed. Since this is not repeatable, you really should always create a `playbook` so that others will know what commands were run and they can run them again simply by running the playbook.

To run a command on all servers use `all` as the target and `-a` followed by the command that you want to run:

    ansible all -a 'sudo apt-get update -y'

This will run `sudo apt-get update -y` on all servers in the `inventory`

## Using Playbooks

But the real power of Ansible is in it's playbooks. To see which tasks will be executed when running a playbook use the `--list-tasks` flag:

    ansible-playbook playbook.yaml --list-tasks

You should see output like the following:
```
playbook: playbook.yaml

  play #1 (all): Performing Package Maintenance on All nodes	TAGS: []
    tasks:
      Update and upgrade local packages	TAGS: []

  play #2 (webservers): 	TAGS: []
    tasks:
      Ensure that Apache is at the latest version	TAGS: []
      Start Apache Services	TAGS: []

  play #3 (dbservers): 	TAGS: []
    tasks:
      Ensure Redis is installed	TAGS: []
      Start Redis	TAGS: []

  play #4 (webservers:dbservers): 	TAGS: []
    tasks:
      Stop UFW NOW!!!	TAGS: []
```

### Using Dry Run mode

You can also run the playbooks in _Dry Run_ mode to check what would be changing if you atually ran it. You would use the `--check` flag to do this:

    ansible-playbook playbook.yaml --check

The check summary will have one failure:
```
PLAY RECAP *********************************************************************
db1                        : ok=2    changed=1    unreachable=0    failed=0
web1                       : ok=5    changed=3    unreachable=0    failed=1
```

That's OK because `apache2` is not installed so it cannot be started.

### Running a playbook

Finally to run the playbook change your servers use:

    ansible-playbook playbook.yaml

This will execute the commands that are in `playbook.yaml` and display output like the following:
```
PLAY [Performing Package Maintenance on All nodes] *****************************

TASK [setup] *******************************************************************
ok: [web1]
ok: [db1]

TASK [Update and upgrade local packages] ***************************************
changed: [db1]
changed: [web1]

PLAY ***************************************************************************

TASK [setup] *******************************************************************
ok: [web1]

TASK [Ensure that Apache is at the latest version] *****************************
changed: [web1]

TASK [Start Apache Services] ***************************************************
ok: [web1]

RUNNING HANDLER [restart apache2] **********************************************
changed: [web1]

PLAY ***************************************************************************

TASK [setup] *******************************************************************
ok: [db1]

TASK [Ensure Redis is installed] ***********************************************
changed: [db1]

TASK [Start Redis] *************************************************************
ok: [db1]

PLAY ***************************************************************************

TASK [setup] *******************************************************************
ok: [web1]
ok: [db1]

TASK [Stop UFW NOW!!!] *********************************************************
changed: [web1]
changed: [db1]

PLAY RECAP *********************************************************************
db1                        : ok=7    changed=3    unreachable=0    failed=0
web1                       : ok=8    changed=4    unreachable=0    failed=0
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

You can also add the `-v` parameter when running a playbook to see the commands that are being executed. Running the following:
```
    ansible-playbook -v playbook.yaml
```
Will run the playbook with _verbose_ output.

## Vagrant and Ansible

You can actually use Ansible to provision your Vagrant vm. The only prerequsite is that you have to already have Ansible installed on your laptop. The easiest way to do this for Python developers is with `pip install ansible`. There is an example at the bottom of the `Vagrantfile` that is commented out. It looks like this:
```
client.vm.provision "ansible" do |ansible|
  ansible.playbook = "python.yaml"
end
```
This will use the `python.yaml` playbook that is included in this repo to provision your vm just like we have done with previous projects using the `shell` provisioner. The difference is that it will use Ansible and be idempotent so that it doesn't try and install things that are already installed like `shell` provisioning will do.

## Experiment

You now have a small multi-server environment on your laptop where you can feel free to explore  more `ansible` commands that you've learned in class.
