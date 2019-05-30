# Zuul Config Job
Provide instruction for using the `Zuul` job in this repo.

###  trigger-build
This job use `webhood` url to trigger the `OpenShift` image build process. Here are the instruction to properly use this `Zuul` job to trigger image build.

**First Step**
Here are the three parameters that is needed to use this `Zuul` job.
- cluster (optional)
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

**Second Step**
Make sure in the `buildConfig-template.yaml` file, the `generic` trigger is added.
Here is the example code add to the `triggers` section
```yaml
- type: "Generic"
  generic:
    secretReference:
      name: "<mysecret>"
```
This is `Generic Webhooks` invoked from any system capable of making a regular web request. Replace the `<mysecret>` with your own `secret`. 

