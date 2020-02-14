#!/bin/bash

create_copy_of_original() {
  file=$1.'orginal'

  if [ -f "$file" ]; then
    echo $file ' already exist'
  else
    cp $1 $file
  fi

  remove_backup $1
}

remove_backup() {
  file=$1.'bk'
  if [ -f "$file" ]; then
    rm $file
  fi

  touch $file
}

#create_copy_of_original "/etc/apache2/httpd.conf"
#create_copy_of_original "/etc/apache2/extra/httpd-userdir.conf"
#create_copy_of_original "/etc/apache2/extra/httpd-vhosts.conf"
#create_copy_of_original "/etc/apache2/users/$(whoami).conf"
#create_copy_of_original "/etc/hosts"
