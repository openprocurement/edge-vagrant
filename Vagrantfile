# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(2) do |config|
  config.vm.box = "fedora/24-cloud-base"
  config.vm.hostname = 'lite-public'

  config.vm.network "forwarded_port", guest: 80, host: 10001 # nginx ("/api/" [GET -> EDGE/Couchdb])
  config.vm.network "forwarded_port", guest: 19999, guiest_ip: "localhost", host: 10009 # NetData

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
  end

  config.vm.provision "shell",
    inline: "sudo dnf install python python-dnf libselinux-python -y"

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.verbose = "v"
    ansible.tags = "all"
    ansible.extra_vars = {
        "edge": true,
        "edge_data_bridge": true
    }
  end
end
