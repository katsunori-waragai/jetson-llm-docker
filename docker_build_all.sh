#!/bin/bash
cwd=$(pwd)
for i in $(echo */docker_build.sh); do
	echo $i
	cd ${cwd}/$(dirname $i)
	sh docker_build.sh
done 
