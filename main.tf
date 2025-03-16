provider "aws" {
  region = "us-east-1"
}

resource "aws_ecs_cluster" "my_cluster" {
  name = "my-cluster"
}

resource "aws_iam_role" "ecs_task_execution" {
  name = "ecsTaskExecutionRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ],
  })
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
  ]
}

resource "aws_ecs_task_definition" "my_task" {
  family                   = "my-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  container_definitions    = jsonencode([
    {
      name  = "my-container"
      image = "my-docker-image:latest"
      essential = true
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"        = "my-log-group"
          "awslogs-region"       = "us-east-1"
          "awslogs-stream-prefix"= "ecs"
        }
      }
      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        },
        {
          name  = "AWS_ACCESS_KEY_ID"
          value = var.aws_access_key_id
        },
        {
          name  = "AWS_ACCOUNT_ID"
          value = var.aws_account_id
        },
        {
          name  = "AWS_CLOUDWATCH_LOGS_ENDPOINT"
          value = var.aws_cloudwatch_logs_endpoint
        },
        {
          name  = "AWS_CLOUDWATCH_LOGS_LOG_GROUP"
          value = var.aws_cloudwatch_logs_log_group
        },
        {
          name  = "AWS_DEFAULT_REGION"
          value = var.aws_default_region
        },
        {
          name  = "AWS_S3_ENDPOINT"
          value = var.aws_s3_endpoint
        },
        {
          name  = "AWS_SECRET_ACCESS_KEY"
          value = var.aws_secret_access_key
        },
        {
          name  = "AWS_SESSION_TOKEN"
          value = var.aws_session_token
        },
        {
          name  = "CORS_ORIGINS"
          value = var.cors_origins
        },
        {
          name  = "FLASK_APP"
          value = var.flask_app
        },
        {
          name  = "FLASK_DEBUG"
          value = var.flask_debug
        }
      ]
      depends_on = [
        "localstack"
      ]
    }
  ])
}

resource "aws_ecs_service" "my_service" {
  name            = "my-service"
  cluster         = aws_ecs_cluster.my_cluster.id
  task_definition = aws_ecs_task_definition.my_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = ["subnet-12345678"]
    security_groups = ["sg-12345678"]
  }
}

variable "environment" {
  description = "The environment in which the service is running"
  type        = string
}

variable "aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
}

variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "aws_cloudwatch_logs_endpoint" {
  description = "AWS CloudWatch Logs Endpoint"
  type        = string
}

variable "aws_cloudwatch_logs_log_group" {
  description = "AWS CloudWatch Logs Log Group"
  type        = string
}

variable "aws_default_region" {
  description = "AWS Default Region"
  type        = string
}

variable "aws_s3_endpoint" {
  description = "AWS S3 Endpoint"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
}

variable "aws_session_token" {
  description = "AWS Session Token"
  type        = string
}

variable "cors_origins" {
  description = "CORS Origins"
  type        = string
}

variable "flask_app" {
  description = "Flask App"
  type        = string
}

variable "flask_debug" {
  description = "Flask Debug"
  type        = string
}