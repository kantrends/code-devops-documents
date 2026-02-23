#!/bin/bash

set -e

JAVA_HOME="{{ java_home }}"
export JAVA_HOME

# you can skip this keystore if your app does not need
rm -rf "{{ app_keystore }}"
echo "`date`:Creating keystore file.."
"${JAVA_HOME}/bin/keytool" -genkey -noprompt \
        -alias tomcat \
        -keyalg RSA -storetype PKCS12 -keysize 2048 -sigalg SHA256withRSA \
        -keystore "{{ app_keystore }}" \
        -dname "CN=`hostname`, OU=QPHCS, O=Premier Inc, L=Charlotte, S=North Carolina, C=US" \
        -storepass premier1 \
        -keypass premier1

# spring datasource variables are stored as ENV variables in the systemd service
echo "`date`: starting application {{ app_location }} .."
cd "{{ app_dir }}"
"${JAVA_HOME}/bin/java" -jar "{{ app_location }}" \
	--server.port=8443 \
	--server.ssl.enabled=true \
	--server.ssl.key-store="{{ app_keystore }}" \
	--server.ssl.key-store-password=premier1 \
	--server.ssl.key-store-type=PKCS12 \
	--server.ssl.key-alias=tomcat \
	>> "{{ app_log_file }}" 2>&1 # redirect both stdout & stderr to file
