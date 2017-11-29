# -*- mode: ruby -*-
# vi: set ft=ruby :

#creating keys allowing inter-cluster ssh
if ARGV[0] == "up"
    puts "Info: attempting to create ssh keys"
    system('./keys/create-keys.sh')
end

# unless Vagrant.has_plugin?("vagrant-guest_ansible")
#   system("vagrant plugin install vagrant-guest_ansible")
#   puts "Ansible dependencies installed, please try the command again."
#   exit
# end

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  # Copy the ssh keys to all of the vms
  if File.exists?(File.expand_path("./keys/id_rsa"))
    config.vm.provision "file", source: "./keys/id_rsa", destination: "~/.ssh/id_rsa"
  end
  if File.exists?(File.expand_path("./keys/id_rsa.pub"))
    config.vm.provision "file", source: "./keys/id_rsa.pub", destination: "~/.ssh/id_rsa.pub"
  end

  config.vm.provision "shell", inline: <<-SHELL
    # add public ssh key to authorized_keys
    cat /home/ubuntu/.ssh/id_rsa.pub >> /home/ubuntu/.ssh/authorized_keys
		chmod 600 /home/ubuntu/.ssh/id_rsa.pub
		chmod 600 /home/ubuntu/.ssh/id_rsa
		chmod 700 /home/ubuntu/.ssh
  SHELL

  # Create the web server
  config.vm.define "web" do |web|
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
    db.vm.hostname = "db"
    db.vm.network "private_network", ip: "192.168.33.30"
    db.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
      vb.cpus = 1
    end
  end

  # Create the ansible client to control servers
  config.vm.define "client" do |client|
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
      # Make vi look nice
      sudo -H -u ubuntu echo "colorscheme desert" > ~/.vimrc
    SHELL

    #
    # Run Ansible using the guest plugin
    #
    # config.vm.provision :guest_ansible do |guest_ansible|
    #   guest_ansible.playbook = "python.yaml"
    #   guest_ansible.extra_vars = extra_vars
    #   guest_ansible.sudo = true
    # end

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

end
