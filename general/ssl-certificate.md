Table of contents
=================

This document covers steps to create Premier SSL certificate for any servers.


## **1. Generate CSR and Key File**

The first step is to create a CSR certificate & key file for your server. 

### **1.1 CSR Configuration File**
   
In order to create a CSR certificate, we need the below configuration file.   Create a file called csr.conf and add the below contents. 
For example, the below configuration file is for server c3happy01.premierinc.com.   You can provide an email address.  Make sure the CN and subjectAltName matches.

```
[ req ]
default_bits = 4096
prompt = no
encrypt_key = no
default_md = sha256
distinguished_name = dn
req_extensions = req_ext

[ dn ]
CN = c3happy01.premierinc.com
emailAddress = cicdteam_alerts@premierinc.com <any custom email id>
O = PREMIER, INC
OU = CODE
L = Charlotte
ST = North Carolina
C = US

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = code-np-ingress.premierinc.com
DNS.2 = *.code-aks-dev.premierinc.com
DNS.3 = *.code-aks-qa.premierinc.com
```
### **1.2 Generate CSR & Keys**

Run the following command to create a key file and a CSR file. 
```
openssl req -new -config csr.conf -keyout server.key -out server.csr
```
Confirm the CSR using this command:
```
openssl req -text -noout -verify -in server.csr
```
## **2. Submit CSR to CA and Get Certificates**

The next step is to submit the CSR to the CA and get it signed.  Premier has a CA authority that signs the certificate and provides new certificates.  

1.	Go to this URL: https://crl.premierinc.com/certsrv/

2.	Select Request a Certificate

3.	Select Submit a Certificate Request

4.	Copy the contents of the CSR file (server.csr) and paste the contents in the text area.

5.	Under the Certificate Template, select the Web Server NES - SHA2

6.	Submit the form now.

7.	On the next page, select Base64 Encoded and click the Download certificate chain.  The Certificates will be downloaded in the P7B format that contains the server certificate, intermediate certificate, and the root certificate,

> **Note** New update: The SSL certificate will be available only after 1 or 2 days. If it gets delayed, check with Chris Maskeri

## **3. Convert the Certificates to PEM format**

Run the below command to convert the P7B certificate Chain to PEM format.  You can now use the key file generated at the beginning and this PEM file to load your certificates.
```
openssl pkcs7 -print_certs -in [cert].p7b -out serverAllCertChain.pem
```
## **3(a). Generate Cert file for Azure Key Vault
```bash
# Merge serverAllCertChain.pem and server.key into a single file, filtering out metadata lines
awk '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/ {print} /-----BEGIN PRIVATE KEY-----/,/-----END PRIVATE KEY-----/ {print}' serverAllCertChain.pem server.key > az_keyvault_cert.pem
```
- Now you can upload the `az_keyvault_cert.pem` to the Azure Key vault using ADO pipeline.


## **4. Generating Keystores**

Some times we need the certificates and key files to be loaded to a Keystore and use that Keystore in our configurations.  Let's see how to create Keystore from the Certificates (PEM) files.

### **4.1 Generate PKCS12 Keystore**

PKCS12 is the industry format.  Always use this format in your configurations.  In case if this format is unsupported, then go for JKS format.
```
openssl pkcs12 -export -name <name> -in <pem file> -inkey <key file> -out <keystore name> -password "pass:<keystore password>"

# For example:
openssl pkcs12 -export -name tomcat -in serverAllCertChain.pem -inkey server.key -out keystore.p12 -password "pass:abcdXXX1"
```
### **4.2 Generate JKS Keystore**

You can create a JKS Keystore from PKCS12 Keystore.  Use the below command to do that.  it will prompt you to enter the new password for JKS Keystore.  It will also prompt for the PKCS12 Keystore password.
```
keytool -importkeystore -srcstoretype pkcs12 -srckeystore <p12 keystore name> -destkeystore <jks keystore name>

# For example:
keytool -importkeystore -srcstoretype pkcs12 -srckeystore keystore.p12 -destkeystore keystore.jks
```
