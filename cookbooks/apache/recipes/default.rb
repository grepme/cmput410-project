package 'apache2'
package 'libapache2-mod-wsgi'
package 'ruby'

service 'apache2' do
    action [:start, :enable]
end