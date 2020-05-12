
# Getting Started

## Authenticate CLI

```
$ sls alexa auth
```

## Create your skill

```
$ sls alexa create --name corona-stats --locale pt-BR --type custom
```

## List existing manifests

```
$ sls alexa manifests
```

## Apply changes (--dryRun is allowed here)

```
$ sls alexa update
```

## Building the interaction model

### The skill does not have an interaction model at first, so you'll need to write an interaction model definition to **serverless.yml**

```
custom:
  alexa:
    vendorId: ${env:AMAZON_VENDOR_ID}
    clientId: ${env:AMAZON_CLIENT_ID}
    clientSecret: ${env:AMAZON_CLIENT_SECRET}
    skills:
      - id: ${env:ALEXA_SKILL_ID}
        manifest:
          publishingInformation:
            locales:
              en-US:
                name: sample
          apis:
            custom: {}
          manifestVersion: '1.0'
        models:
          en-US:
            interactionModel:
              languageModel:
                invocationName: PPAP
                intents:
                  - name: PineAppleIntent
                    slots:
                    - name: Fisrt
                      type: AMAZON.Food
                    - name: Second
                      type: AMAZON.Food
                    samples:
                     - 'I have {First} and {Second}'
```

### Build the model (--dryRun is allowed here)

```
$ sls alexa build
```

### Check the model

```
sls alexa models
```

# References

[Develop console](https://developer.amazon.com/dashboard)

[How To Manage Your Alexa Skills With Serverless](https://www.serverless.com/blog/how-to-manage-your-alexa-skills-with-serverless/)

[To find your Vendor ID](https://developer.amazon.com/mycid.html)
