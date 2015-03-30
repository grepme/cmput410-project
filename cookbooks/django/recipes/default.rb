python_pip "django"
python_pip "commonmark
python_pip "pillow"
python_pip "beautifulsoup4"
python_pip "feedparser"

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
		<Location /api>
			AuthType basic
			AuthName \"Secure API\"
			AuthBasicProvider dbm
			AuthDBMType SDBM
			AuthDBMUserFile /vagrant/api_password_file
			Require valid-user
		</Location>
		Alias /static/ /vagrant/static/
    </VirtualHost>"
end

execute "a2enmod" do
	command "a2enmod authn_dbm"
	action :run
end

execute "a2ensite" do
    command "a2ensite project"
    action :run
end

execute "service" do
    command "service apache2 reload"
    action :run
end