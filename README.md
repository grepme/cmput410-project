# CMPUT 410 Project

A base example of a social network.

# Do I Need Vagrant?

No.

python manage.py runserver

Go to town, work from localhost. You may run into issues with a different environment and MySQL if we choose to
migrate. You have been warned.

# Vagrant Installation

[Download and install Vagrant](https://www.vagrantup.com/downloads.html)

Make sure you have Vagrant 1.7.2
```bash
vagrant version
```

Install vagrant-omnibus and put the virtual machine online. It can take up to fifteen minutes to download
and install all the packages.
```bash
vagrant plugin install vagrant-omnibus
vagrant up
```
The provisioning can take awhile to install, but once done, project is viewable on 
[localhost:8080](http://localhost:8080).

All changes on your local machine update in real-time on the virtual machine!

# Important Tips

* I left on sqlite3, we may migrate to MySQL later. It is installed with root password of 'SomethingSpecial'.
* You can ssh to the virtual machine with: vagrant ssh
* Django is in debug mode. However, sometimes Python errors will not show and Apache will throw a 5xx error. Run: sudo tail /var/log/apache2/error.log
* The apache2 configuration is located at: /etc/apache2/sites-enabled/project
* Need to restart the httpd to see changes that don't auto-update? Run: sudo service apache2 restart
* All files are located on /vagrant on the virtual machine.

# Github Pages
Our API can be found at:
http://grepme.github.io/cmput410-project
