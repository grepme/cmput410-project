mysqld CHANGELOG
================

This file is used to list changes made in each version of the mysqld cookbook.

1.0.0
-----

- Add support for mariadb
- Add support for mariadb-galera
- Automatically set admin passwords if attribute is given (incl. modifying `/etc/mysql/debian.cnf`
  accordingly, if required)

Compatibility changes:

- Rename `node['mysqld']['packages']` attribute to `node['mysqld']['mysql_packages']`

0.3.0
-----

- Add support to remove configuration options set by default attributes

0.2.0
-----
- Do not manage `service_name`, when `service_name` is empty
- Fixes an issue with the template when the LWRP was called from another cookbook
- Use `deep_merge` to merge my.cnf hashes

0.1.0
-----
- Initial release of mysqld
