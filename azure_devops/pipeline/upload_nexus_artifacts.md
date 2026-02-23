# Purpose
This section covers steps to be followed for uploading artifacts to Nexus. 

# Table of Contents
- [Maven JAR](#maven-jar)
- [Python PYPI](#python-pypi)
- [DotNet NuGet](#dotnet-nuget)
- [NPM](#npm)

# Maven JAR
In order to upload Nuget Package to Nexus, add below configuration in your pom.xml file:
```yaml
<distributionManagement>
        <repository>
            <id>nexus-artifacts</id>
            <url>
                https://nexus.premierinc.com/artifacts/repository/releases
            </url>
        </repository>
        <snapshotRepository>
            <id>nexus-artifacts</id>
            <url>
                https://nexus.premierinc.com/artifacts/repositories/snapshots
            </url>
        </snapshotRepository>
    </distributionManagement>
```
Use below pipeline task:
```yaml
        - task: Maven@4
          displayName: Maven Build
          inputs:
            mavenPomFile: 'pom.xml'
            goals: 'clean deploy'
            options: '-B -Dmaven.test.skip'
            javaHomeOption: 'Path'
            jdkDirectory: $(SYSTEM_JDK_8)
            mavenVersionOption: 'Path'
            mavenDirectory: $(SYSTEM_MAVEN_3_HOME)
```
`goals: 'clean deploy'` will push your build artifact to Nexus Artifacts.

| index | url | description | 
| -- | -- | -- |
| releases | https://nexus.premierinc.com/artifacts/repository/releases/ | Can be pushed only once |
| snapshots | https://nexus.premierinc.com/artifacts/repository/snapshots/ | Can be pushed multiple times and overwrite packages |

# Python PYPI
| index | url | description | 
| -- | -- | -- |
| premier-pypi | https://nexus.premierinc.com/artifacts/repository/premier-pypi/ | Can be pushed only once |
| premier-pypi-snapshots | https://nexus.premierinc.com/artifacts/repository/premier-pypi-snapshots/ | Can be pushed multiple times and overwrite packages |

```bash
# To upload release versions
twine upload -r premier-pypi <filename>

# To upload snapshots or development versions
twine upload -r premier-pypi-snapshots <filename>
```

# DotNet NuGet
In order to upload Nuget Package to Nexus, use the below Pipeline Task:

```YAML
  - task: NuGetCommand@2
    inputs:
      command: 'push'
      packagesToPush: '$(Build.ArtifactStagingDirectory)/**/*.nupkg;!$(Build.ArtifactStagingDirectory)/**/*.symbols.nupkg'
      nuGetFeedType: 'external'
      publishFeedCredentials: 'Nexus_Nuget-Inflow'
```

`Nexus_Nuget-Inflow` is the name of the service connection of type "NuGet" configured in the Azure DevOps Project.  If not configured, please create a [snow ticket](https://premierprod.service-now.com/premiernow?id=dept_cat_item&sys_id=d7f4cf011bbd3450be08975e034bcb58) on our team to configure it for you.  We created one service connection in CODE ADO project and then shared the same connection across other projects in Azure DevOps. 

# NPM
Publish NPM packages to Nexus. The Nexus NPM Registries URL and credentials are configured on the Build Agents. 
| Repository | URL | Description
| --- | --- | --- |
| premier-npm | https://nexus.premierinc.com/artifacts/repository/premier-npm/ | - Publish same version multiple times and overwrite package.<br>- Packages in this repositories are short lived and will be deleted as per our cleanup policy.<br> **Note**: Use this only for development purpose. | 
| premier-npm-releases | https://nexus.premierinc.com/artifacts/repository/premier-npm-releases | A version can be published only once.<br>**Note**: Use this for production release. |

- Remove the publish Config from package.json file so that your pipeline will have the ability to choose the registry at run-time. 
  ```yaml
  # package.json file
  {
    "private": false
    # remove this publishConfig if you have
    "publishConfig": {
      "registry": "http://nexus.premierinc.com/artifacts/repository/premier-npm/"
    }
    ...
  }
  ```
- Pipeline changes in YAML file. Based on the branch, choosing the NPM Registry. 
  ```YAML
  # pipeline YAML file
  - bash: |
      set -e

      # considering "main" branch is production branch of this repo.
      if [[ "${{ variables['Build.SourceBranch'] }}" = "refs/heads/main" ]] ; then
          NPM_REGISTRY="https://nexus.premierinc.com/artifacts/repository/premier-npm-releases/"
      else
          NPM_REGISTRY="https://nexus.premierinc.com/artifacts/repository/premier-npm/"
      fi
      npm publish --verbose --access public --registry "$NPM_REGISTRY"
      echo "Publishing to NPM Registry: $NPM_REGISTRY is completed successfully !!!"
    displayName: Publish NPM Package to Nexus
  ```

