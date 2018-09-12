#!/bin/bash

echo 'deleting TDAP_Test_Run child folder'
rm -rf TDAP_Test_Run

echo 'deleting TDAP_Test_Run.zip'
rm TDAP_Test_Run.zip

echo 'creating TDAP_Test_Run child directory'
mkdir TDAP_Test_Run

echo 'copying custom-recipes into TDAP_Test_Run'
cp -R custom-recipes TDAP_Test_Run/ 

echo 'copying js into TDAP_Test_Run'
cp -R js TDAP_Test_Run/

echo 'copying python-lib into TDAP_Test_Run'
cp -R python-lib TDAP_Test_Run/

echo 'copying resource into TDAP_Test_Run'
cp -R resource TDAP_Test_Run/

echo 'copying plugin.json into TDAP_Test_Run'
cp plugin.json TDAP_Test_Run/

echo 'zipping TDAP_Test_Run'
zip -r "TDAP_Test_Run.zip" "TDAP_Test_Run"
