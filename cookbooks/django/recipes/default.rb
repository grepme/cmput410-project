python_pip "django"

file "/etc/apache2/sites-available/project" do
    action :create
    content "WSGIPythonPath /vagrant
    <VirtualHost *:80>
        ServerName localhost:8080
        WSGIScriptAlias / /vagrant/social_network/wsgi.py

        <Directory /vagrant/social_network>
            <Files wsgi.py>
                 Allow from all
            </Files>
        </Directory>
    </VirtualHost>"
end

execute "a2enmod" do
    command "a2ensite project"
    action :run
end

execute "service" do
    command "service apache2 reload"
    action :run
end