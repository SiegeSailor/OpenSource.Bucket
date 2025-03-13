# Overview

This is a backend service project that provides a RESTful interface for AWS S3 using Flask. Following the Microservices Principle, this project has been wrapped with Docker, LocalStack, and Terraform to isolate the running/deploying environments with a fully configurable layer that support development on the local laptops, testing in CI/CD pipelines, and deployment to the AWS services.

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

| Environment Variable            | Description                                                                                          |
| ------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `AWS_ACCESS_KEY_ID`             | Available on [AWS Account Overview](https://console.aws.amazon.com/).                                |
| `AWS_ACCOUNT_ID`                | A 12-digit number. Available on [AWS Account Overview](https://console.aws.amazon.com/).             |
| `AWS_CLOUDWATCH_LOGS_ENDPOINT`  | AWS CloudWatch Logs service endpoint.                                                                |
| `AWS_CLOUDWATCH_LOGS_LOG_GROUP` | The log group name for logs generated in this project.                                               |
| `AWS_DEFAULT_REGION`            | Default AWS region.                                                                                  |
| `AWS_S3_BUCKET`                 | The top-level bucket name for all buckets and files uploaded through this project.                   |
| `AWS_S3_ENDPOINT`               | AWS S3 service endpoint.                                                                             |
| `AWS_SECRET_ACCESS_KEY`         | Available on [AWS Account Overview](https://console.aws.amazon.com/).                                |
| `AWS_SESSION_TOKEN`             | Available with [AWS STS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html). |
| `ENVIRONMENT`                   | Accept `development`, `testing`, and `production`.                                                   |
| `LOCALSTACK_AUTH_TOKEN`         | Available on [LocalStack Auth Tokens](https://app.localstack.cloud/workspace/auth-tokens).           |

## Prerequesites

- Docker: `Docker version 28.0.1, build 068a01e`

## Local Development

Create a `.env` in the root directory:

```conf
AWS_ACCESS_KEY_ID=dummy
AWS_ACCOUNT_ID=000000000000
AWS_CLOUDWATCH_LOGS_ENDPOINT=http://localstack:4566
AWS_CLOUDWATCH_LOGS_LOG_GROUP=bucket
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET=bucket
AWS_S3_ENDPOINT=http://localstack:4566
AWS_SECRET_ACCESS_KEY=test
AWS_SESSION_TOKEN=test
ENVIRONMENT=development
LOCALSTACK_AUTH_TOKEN=
```

> Most of the credential and cloud service values can be random since the local development environment is isolated and will be flushed every time the environment shuts down. See [Configurable Environment Variables](#configurable-environment-variables).

Start developing with hot-loading and console logging enabled:

```bash
docker compose \
    up --abort-on-container-exit --build --force-recreate
docker compose \
    down
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
