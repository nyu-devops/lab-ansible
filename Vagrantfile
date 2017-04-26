# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  # Create the web server
  config.vm.define "web" do |web|
    web.vm.box = "ubuntu/trusty64"
    web.vm.hostname = "web"
    web.vm.network "private_network", ip: "192.168.33.20"
    web.vm.network "forwarded_port", guest: 80, host: 8080
    web.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.cpus = 1
    end
  end

  # Create the db server
  config.vm.define "db" do |db|
    db.vm.box = "ubuntu/trusty64"
    db.vm.hostname = "db"
    db.vm.network "private_network", ip: "192.168.33.30"
    db.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.cpus = 1
    end
  end

  # Create the ansible client to control servers
  config.vm.define "client" do |client|
    client.vm.box = "ubuntu/trusty64"
    client.vm.hostname = "client"
    client.vm.network "private_network", ip: "192.168.33.10"
    client.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.cpus = 1
    end
    # Install required application libraries
    client.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update
      sudo apt-get install -y ansible sshpass tree
      sudo apt-get -y autoremove
      # Add the other servers to the hosts file as if we had a DNS
      sudo echo "192.168.33.20   web1" >> /etc/hosts
      sudo echo "192.168.33.30   db1" >> /etc/hosts
      # Create an ssh key pair as vagrant user
        #   sudo -H -u vagrant ssh-keygen -t rsa -C "vagrant@ansible.com" -f /home/vagrant/.ssh/id_rsa -N ""
        #   sshpass -p 'vagrant' ssh-copy-id -i /home/vagrant/.ssh/id_rsa vagrant@192.168.33.20
        #   sshpass -p 'vagrant' ssh-copy-id -i /home/vagrant/.ssh/id_rsa vagrant@192.168.33.30
      # Make vi look nice
      sudo -H -u vagrant echo "colorscheme desert" > ~/.vimrc
    SHELL
  end

end
