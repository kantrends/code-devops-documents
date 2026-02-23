# Use Nexus in Local Workstation
According to Premier standards, all the 3rd party libraries have to be pulled from Nexus and not from internet. All CICD Pipelines are configured to use Nexus Repository Manager to download libraries. This document covers steps on how to configure the Nexus URLs in your local workstation so that the developer's work environment is similar to pipeline environment.  This avoids the most common issue where the build works well in local but not in pipeline. 

# Table of Contents

- [NPM](#npm)
- [Maven](#maven)
- [Python](#python)
- [NuGet](#nuget)
- [FAQ](#faq)

# NPM
In order for the NPM to use Nexus to download the package, create a file `$HOME/.npmrc` with the below contents. 
```
registry=https://nexus.premierinc.com/artifacts/repository/npm
``` 
In case, if your project already has package-lock.json file configured with Internet Proxy URL, then you have to recreate the package-lock.json with Nexus URL. 

# Maven
Create a file `$HOME/.m2/settings.xml` with below contents
```XML
<?xml version="1.0" encoding="UTF-8"?>

<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">

    <mirrors>
        <mirror>
            <id>nexus-public</id>
            <mirrorOf>external:*,!nexus-artifacts-snapshots,!nexus-artifacts-releases</mirrorOf>
            <url>https://nexus.premierinc.com/artifacts/repository/public</url>
        </mirror>
    </mirrors>


    <profiles>
        <profile>
            <id>nexus-platform</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>

            <repositories>
                <repository>
                    <id>central</id>
                    <url>https://nexus.premierinc.com/artifacts/repository/public</url>
                    <releases>
                        <enabled>true</enabled>
                        <updatePolicy>never</updatePolicy>
                    </releases>
                    <snapshots>
                        <enabled>true</enabled>
                        <!--<updatePolicy>always</updatePolicy>-->
                    </snapshots>
                </repository>
                <repository>
                    <id>nexus-artifacts-releases</id>
                    <url>https://nexus.premierinc.com/artifacts/repository/releases-group</url>
                    <releases>
                        <enabled>true</enabled>
                        <updatePolicy>interval:20</updatePolicy>
                    </releases>
                    <snapshots>
                        <enabled>false</enabled>
                    </snapshots>
                </repository>
            </repositories>
            <pluginRepositories>
                <pluginRepository>
                    <id>central</id>
                    <url>https://nexus.premierinc.com/artifacts/repository/public</url>
                    <releases>
                        <enabled>true</enabled>
                        <updatePolicy>never</updatePolicy>
                    </releases>
                    <snapshots>
                        <enabled>true</enabled>
                        <!--<updatePolicy>always</updatePolicy>-->
                    </snapshots>
                </pluginRepository>
                <pluginRepository>
                    <id>nexus-artifacts-snapshots</id>
                    <url>https://nexus.premierinc.com/artifacts/repository/snapshots-group</url>
                    <releases>
                        <enabled>true</enabled>
                        <updatePolicy>interval:20</updatePolicy>
                    </releases>
                    <snapshots>
                        <enabled>true</enabled>
                        <!--<updatePolicy>always</updatePolicy>-->
                    </snapshots>
                </pluginRepository>
            </pluginRepositories>
        </profile>
    </profiles>

</settings>
```

# Python

- Linux users, create a file `$HOME/.pip/pip.conf` with below contents:
- Windows users, create file `%APPDATA%\pip\pip.ini` with below contents:
```INI
[global]
index = https://nexus.premierinc.com/artifacts/repository/pypi/pypi
index-url = https://nexus.premierinc.com/artifacts/repository/pypi/simple
```

# NuGet
Create a file `%APPDATA%/NuGet/NuGet.Config` with below contents:

```XML
<?xml version="1.0" encoding="utf-8"?>
<configuration>
	<config>
		<add key="DefaultPushSource" value="https://nexus.premierinc.com/artifacts/repository/nuget-releases" />
	</config>
	
	<packageSources>
		<add key="Nexus" value="https://nexus.premierinc.com/artifacts/repository/nuget-group/index.json" />
		<add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
	</packageSources>
	
	<disabledPackageSources>
		<add key="nuget.org" value="true" />
	</disabledPackageSources>
	
	<activePackageSource>
		<add key="All" value="(Aggregate source)" />
	</activePackageSource>
	
</configuration>
```

# FAQ
**1. What is $HOME?**

$HOME variable contains the path to the user's home directory. To find your home directory:
- Windows users, run the below command in powershell
  ```
  PS E:\aselvara> $HOME
  E:\aselvara
  PS E:\aselvara>
  ```
- Mac/Linux users, run the below command in terminal:
  ```
  $> echo $HOME
  /home/aselvara
  $>
  ```
