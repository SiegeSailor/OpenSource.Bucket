# Overview

This is a backend service project that provides a RESTful interface for AWS S3 using Flask. Following the Microservices Principle, this project has been wrapped with Docker, LocalStack, and Terraform to isolate the running/deploying-environments with a fully configurable layer that support development on the local laptops, testing in CI/CD pipelines, and deployment to the AWS services.

## RESTful Interface

This backend service comes with the following endpoints:

| HTTP Method | Path                        | Description                |
| ----------- | --------------------------- | -------------------------- |
| GET         | `/`                         | Check if Flask is running. |
| POST        | `/file/`                    | Upload a file.             |
| GET         | `/file/<bucket>/<filename>` | Generate a file URL.       |
| DELETE      | `/file/<bucket>/<filename>` | Delete a file.             |

## Configurable Environment Variables

The varaibles below have been wrapped in development and automation tools, such as Docker Compose and GitHub Actions:

| Environment Variable            | Description                                                                                                                                                                                     |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`             | The access key id of AWS. It is available on [AWS Account Overview](https://console.aws.amazon.com/).                                                                                           |
| `AWS_ACCOUNT_ID`                | A 12-digit number. It is available on [AWS Account Overview](https://console.aws.amazon.com/).                                                                                                  |
| `AWS_CLOUDWATCH_LOGS_ENDPOINT`  | AWS CloudWatch Logs service endpoint.                                                                                                                                                           |
| `AWS_CLOUDWATCH_LOGS_LOG_GROUP` | The log group name for logs generated in this project.                                                                                                                                          |
| `AWS_DEFAULT_REGION`            | Default AWS region.                                                                                                                                                                             |
| `AWS_S3_ENDPOINT`               | AWS S3 service endpoint.                                                                                                                                                                        |
| `AWS_SECRET_ACCESS_KEY`         | The secret access key of AWS. It is available on [AWS Account Overview](https://console.aws.amazon.com/).                                                                                       |
| `AWS_SESSION_TOKEN`             | The session token of AWS. It is available with [AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html).                                                            |
| `CORS_ORIGINS`                  | Allowed origins for Flask. This is a string separated with `,` and doesn't work with pre-signed URLs.                                                                                           |
| `ENVIRONMENT`                   | Accept `development`, `testing`, and `production`.                                                                                                                                              |
| `LOCALSTACK_AUTH_TOKEN`         | Serving this enables the LocalStack dashboard communicating with the local environment. The token is available on [LocalStack Auth Tokens](https://app.localstack.cloud/workspace/auth-tokens). |

## Development

Configure a local development environment.

## Prerequesites

- Docker: `Docker version 28.0.1, build 068a01e`
- Terraform: `Terraform v1.11.2`
- AWS: `aws-cli/2.24.24`

Create a `.env` in the root directory:

```conf
AWS_ACCESS_KEY_ID=dummy
AWS_ACCOUNT_ID=000000000000
AWS_CLOUDWATCH_LOGS_ENDPOINT=http://localstack:4566
AWS_CLOUDWATCH_LOGS_LOG_GROUP=file-service
AWS_DEFAULT_REGION=us-east-1
AWS_S3_ENDPOINT=http://localstack:4566
AWS_SECRET_ACCESS_KEY=test
AWS_SESSION_TOKEN=test
CORS_ORIGINS=*
ENVIRONMENT=testing
LOCALSTACK_AUTH_TOKEN=
```

> Most of the credential and cloud service values can be random since the local development environment is isolated and will be flushed every time the environment shuts down. See [Configurable Environment Variables](#configurable-environment-variables).

Start developing with hot-loading and console logging enabled:

```bash
docker compose up \
    --abort-on-container-exit --build --force-recreate
docker compose down
```

A folder `./volume` will be created in the root directory, which stores persistent data for LocalStack:

```
└── 📁source/
└── 📁test/
└── 📁volume/
└── .env
└── .gitignore
└── docker-compose.yml
└── Dockerfile
└── ...
```

You should see something similar below in the Docker Compose shell. The local environment is now ready:

```
localstack-1  | 2025-03-13T19:12:37.316  INFO --- [et.reactor-0] localstack.request.aws     : AWS logs.DescribeLogGroups => 200
localstack-1  | 2025-03-13T19:12:37.479  INFO --- [et.reactor-0] localstack.request.aws     : AWS logs.CreateLogGroup => 200
localstack-1  | 2025-03-13T19:12:37.482  INFO --- [et.reactor-0] localstack.request.aws     : AWS logs.DescribeLogGroups => 200
flask-1       |  * Serving Flask app 'main:create_main'
flask-1       |  * Debug mode: on
flask-1       | INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
flask-1       |  * Running on all addresses (0.0.0.0)
flask-1       |  * Running on http://127.0.0.1:5000
flask-1       |  * Running on http://172.18.0.3:5000
flask-1       | INFO:werkzeug:Press CTRL+C to quit
```

## Testing

Unit testing and integration testing have been integrated into the GitHub Actions pipelines and only happen there. Due to the fact that the project focuses on utilizing AWS services, manually running the test scripts locally without proper fixtures will not be sufficient.

## Production

Create a `terraform.tfvars` file in the root directory:

```conf
aws_access_key_id     = "<your_aws_access_key_id>"
aws_secret_access_key = "<your_aws_secret_access_key>"
aws_account_id        = "<your_aws_account_id>"
aws_cloudwatch_logs_log_group = "fileservice_log_group"
aws_default_region    = "us-east-1"
environment           = "development"
cors_origins          = "*"
flask_app             = "main:create_main"
flask_debug           = "1"
```

Apply the changes:

```bash
terraform init
terraform apply
```

The changes include the ECR creation. You will have to manually push the Docker to it:

```bash
export REGION=""
export AWS_ACCOUNT_ID=""
docker build --tag fileservice:latest .
docker tag fileservice:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/fileservice:latest
aws ecr get-login-password --region $REGION --profile default | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/fileservice:latest
```

Apply the changes again:

```bash
terraform apply
```

### Destroy Resources

```terraform
provider "aws" {
  region = "us-east-1"
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
}


variable "aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
}
```

```bash
terraform init
terraform apply \
  -var "aws_access_key_id=<your-aws_access_key_id>"
  -var "aws_secret_access_key=<your-aws_secret_access_key>"
```

## Miscellaneous

Some improvement to make to shape this project structure more meaningful. Yet, not required at this moment:

- Logs format
- Routes and directory naming, including Dockerfile, Docker commands, test files
- Plain file structure
- CloudWatch Logs logger handler creation condition
- File uploading should be a PUT method
- API document generation
- Test result generation
- Pipeline and version badges
- Prefix for bucket names
- Module Terraform files
- Automate Terraform
- Automated linting and formatting
