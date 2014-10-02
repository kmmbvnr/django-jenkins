#!/bin/bash

trap 'mysqladmin -u root -proot shutdown' EXIT

mysqld_safe