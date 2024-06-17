#!/bin/bash

# Please set the following arguments to match your settings.
PROFILE="my_profile"
FILTER="project=MYPROJ"
MAX=5
echo "Please set the variables inside this file."
echo

# Define and execute the command
command="pyJiraCli --verbose --profile $PROFILE search $FILTER --max $MAX"

echo "Executing...."
echo $command
echo
$command
