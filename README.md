# Zuul Config

Configuration for Thoth Zuul Instance

## Integration of Zuul with Github Repos

Thoth could be easily integrated in Github Organizations or in Individual Github Repositories.

**Steps to Integrate zuul to Thoth Station Repository**:

- Add a `.zuul.yaml` file with following content with appropriate values. Zuul uses this yaml file to setup the Configuration required for the Repository

```
- project:
    check:
      jobs:
        - thoth-coala
        - thoth-pytest
    gate:
      jobs:
        - "thoth-coala"
    post:
      jobs:
        - "trigger-build":
            vars:
              cluster: ""
              namespace: ""
              buildConfigName: ""
```

- Add a '.coafile' file with following content.Modify it as per requirement, coafile file would be used for configuration on coala test run.

```
[all]
bears = LineCountBear, FilenameBear
files = **.py, **.yaml, **.toml, **.rst, **.md
file_naming_convention = snake
ignore = **/__pycache__/**, **/__pycache__, __pycache__, __pycache__/**, **/*.pyc, *.pyc, .github/**/*.md, test/**
max_line_length = 120
max_lines_per_file = 2000

[all.python]
bears = PycodestyleBear, PyDocStyleBear
files = **.py
language = Python
editor = vim
ignore = setup.py, tests/**,docs/source/conf.py

[zuul.yaml]
bears = YAMLLintBear
files = .zuul.yaml
max_line_length = 180
```

- Add the configuration to [zuul-config](https://github.com/thoth-station/zuul-config) repo, add a config file in the following format and named as the Repository name in [zuul-config/zuul](https://github.com/thoth-station/zuul-config/tree/master/zuul)

```
---
- tenant:
    name: 'local'
    source:
      github.com:
        untrusted-projects:
          - my-project-repo-name
```

**Steps to Integrate in Github Organiztions or Repositories outside Thoth**:

- Thoth Zuul has to be integrated as Github Integration services.<br>
  GoTo Organizations or Repository setting -> integrations & services -> configure zuul-app -> Add Thoth-Zuul.
- Configure it for the Repositories required
- Follow the above steps in _Steps to Integrate zuul to Thoth Station Repository_ to complete the setup.
- voila, zuul is now at your service.

## Zuul Config Job

Provide instruction for using the `Zuul` job in this repo.

### Trigger-build

This job allows user to invoke the `OpenShift` image generic webhook to rebuild the image. Here are the instructions for properly use this `Zuul` job in your project.

**First Step** Here are the three parameters that is required in the `.zuul.yaml` file for determining which webhook your would like to invoke.

- cluster (optional default is set to `paas.psi.redhat.com`)
- namespace (requird)
- buildConfigName (required)

For example, here is an example about how to use this `Zuul` job in `.zuul.yaml` file.

```yaml
post:
  jobs:
    - "trigger-build":
        vars:
          cluster: "paas.psi.redhat.com"
          namespace: "thoth-test-core"
          buildConfigName: "user-api"
```

**Second Step** Make sure in the `BuildConfig` template the `generic` trigger is added. Here is the content to be included in the `trigger` section of the `BuildConfig`. The secret `generic-webhook-secret` is a prerequisite for this generic webhook to work ,which has already been set up on `thoth-test-core` project, no further modification of this content is needed.

```yaml
- type: "Generic"
  generic:
    secretReference:
      name: generic-webhook-secret
```

**Third Step** After changing the `BuildConfig` in your template, remember to upload the updated template to your openshift namespace. For example, you can use the following command to upload your new template.

```
oc apply -f openshift/buildConfig-template.yaml
```
