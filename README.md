# Zuul Config


## Zuul Config Job
Provide instruction for using the `Zuul` job in this repo.

###  trigger-build
This job allows user to invoke the `OpenShift` image generic webhook to rebuild the image. Here are the instructions for properly use this `Zuul` job in your project.

**First Step**
Here are the three parameters that is required in the `.zuul.yaml` file for determining which webhook your would like to invoke.
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

**Second Step**
Make sure in the `BuildConfig` template the `generic` trigger is added.
Here is the content to be included in the `trigger` section of the `BuildConfig`. The secret `generic-webhook-secret` is a prerequisite for this generic webhook to work ,which has already been set up on `thoth-test-core` project, no further modification of this content is needed.
```yaml
- type: "Generic"
  generic:
    secretReference:
      name: generic-webhook-secret
```

**Third Step**
After changing the `BuildConfig` in your template, remember to upload the updated template to your openshift namespace. For example, you can use the following command to upload your new template.
```
oc apply -f openshift/buildConfig-template.yaml
```
