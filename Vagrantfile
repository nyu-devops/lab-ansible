# -*- mode: ruby -*-
# vi: set ft=ruby :

# Commented out because it doesn't work for Windows clients
#creating keys allowing inter-cluster ssh
# if ARGV[0] == "up"
#     puts "Info: attempting to create ssh keys"
#     system('./keys/create-keys.sh')
# end

# # WARNING: You will need the following plugin:
# # vagrant plugin install vagrant-guest_ansible
# if Vagrant.plugins_enabled?
#   unless Vagrant.has_plugin?('vagrant-guest_ansible')
#     puts 'Plugin missing.'
#     system('vagrant plugin install vagrant-guest_ansible')
#     puts 'Ansible dependencies installed, please try the command again.'
#     exit
#   end
# end

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # WARNING: DO NOT UPGRADE BOX
  # Newer versions of Ubuntu already contain python so ping will not fail
  config.vm.box = "ubuntu/bionic64"
  config.vm.synced_folder "./", "/vagrant", owner: "vagrant", mount_options: ["dmode=755,fmode=644"]

  ############################################################
  # Copy some host files to configure VM like the host
  ############################################################

  # Copy the ssh keys to all of the vms
  if File.exist?(File.expand_path("./keys/id_rsa"))
    config.vm.provision "file", source: "./keys/id_rsa", destination: "~/.ssh/id_rsa"
  end
  if File.exist?(File.expand_path("./keys/id_rsa.pub"))
    config.vm.provision "file", source: "./keys/id_rsa.pub", destination: "~/.ssh/id_rsa.pub"
  end

  # Copy your .vimrc file so that your VI editor looks right
  if File.exist?(File.expand_path("~/.vimrc"))
    config.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
  end

  config.vm.provision "shell", inline: <<-SHELL
    # add public ssh key to authorized_keys
    cat /home/vagrant/.ssh/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
    chmod 644 /home/vagrant/.ssh/id_rsa.pub
    chmod 600 /home/vagrant/.ssh/id_rsa
    chmod 700 /home/vagrant/.ssh
  SHELL

  ##################################################
  # Create the ansible client to control servers
  ##################################################
  config.vm.define "client" do |client|
    client.vm.hostname = "client"
    client.vm.network "private_network", ip: "192.168.56.40"
    client.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"

    client.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
      vb.cpus = 1
    end
    
    client.vm.provider "docker" do |docker, override|
      override.vm.box = nil
      docker.image = "rofrano/vagrant-provider:debian"
      docker.remains_running = true
      docker.has_ssh = true
      docker.privileged = true
      docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:rw"]
      docker.create_args = ["--cgroupns=host"]
    end
  
    # Install required application libraries
    client.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update
      sudo apt-get install -y ansible sshpass tree
      sudo apt-get -y autoremove
      # Add the other servers to the hosts file as if we had a DNS
      sudo echo "192.168.56.20   web1" >> /etc/hosts
      sudo echo "192.168.56.30   db1" >> /etc/hosts
    SHELL

    #
    # Run Ansible from the Vagrant Host
    #
    # You can use Ansible to provision vm's but you need to have
    # it installed on your laptop first. The easiest was is with pip
    #    sudo pip install ansible
    #
    # Uncomment the next 3 lines to provision a vm with Ansible
    # client.vm.provision "ansible" do |ansible|
    #   ansible.playbook = "python.yaml"
    # end

  end

  ##################################################
  # Create the web server
  ##################################################
  config.vm.define "web" do |web|
    web.vm.hostname = "web"
    web.vm.network "private_network", ip: "192.168.56.20"
    web.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

    web.vm.provider "virtualbox" do |vb|
      vb.memory = "768"
      vb.cpus = 1
    end
    
    web.vm.provider "docker" do |docker, override|
      override.vm.box = nil
      docker.image = "rofrano/vagrant-provider:debian"
      docker.remains_running = true
      docker.has_ssh = true
      docker.privileged = true
      docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:rw"]
      docker.create_args = ["--cgroupns=host"]
    end
  
  end

  ##################################################
  # Create the db server
  ##################################################
  config.vm.define "db" do |db|
    db.vm.hostname = "db"
    db.vm.network "private_network", ip: "192.168.56.30"

    db.vm.provider "virtualbox" do |vb|
      vb.memory = "768"
      vb.cpus = 1
    end

    db.vm.provider "docker" do |docker, override|
      override.vm.box = nil
      docker.image = "rofrano/vagrant-provider:debian"
      docker.remains_running = true
      docker.has_ssh = true
      docker.privileged = true
      docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:rw"]
      docker.create_args = ["--cgroupns=host"]
    end

  end

  # # Create a Python server
  # config.vm.define "python" do |db|
  #   db.vm.hostname = "python"
  #   db.vm.network "private_network", ip: "192.168.56.40"
  #   db.vm.provider "virtualbox" do |vb|
  #     vb.memory = "256"
  #     vb.cpus = 1
  #   end
  #   #
  #   # Run Ansible using the guest plugin
  #   #
  #   config.vm.provision :guest_ansible do |guest_ansible|
  #     guest_ansible.playbook = "python.yaml"
  #     guest_ansible.extra_vars = { user: "vagrant" }
  #     guest_ansible.sudo = true
  #   end
  # end

end
