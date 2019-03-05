#!/usr/bin/env bash


if [[ ! -e /var/project/pip_install_dev_deps_done ]];
then
    echo "Wait pip finish the installation of requirements/local.txt"
    echo -n "Waiting "
fi

while [[ ! -e /var/project/pip_install_dev_deps_done ]];
do
    echo -n "."
    sleep 2;
done

echo ""

pytest --cache-clear "${@}"
exit $?

