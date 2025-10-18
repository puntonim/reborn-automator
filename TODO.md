- `serverless.yml`
  - sls remove
  - `runtime: python3.13`
  - remove `serverless-iam-roles-per-function`
  - `cron-book-class:` > `cron-book-cali-class:`
  - `stage: production` to `prod`
  - `arn:aws:lambda:${self:provider.region}:017000801446:layer:AWSLambdaPowertoolsPythonV3-python313-x86_64:18`
  - compare the whole file with the one in `alarm-be`

- move botte to a standalone project?
