#!/bin/bash

watchmedo shell-command --patterns "*.py" --command "./restart-pyclient-containers.sh" "../../microservices/python/" &
