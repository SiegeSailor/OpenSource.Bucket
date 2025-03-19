provider "aws" {
  region     = "us-east-1"
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
}

resource "aws_vpc" "fileservice_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_ecr_repository" "fileservice" {
  name = "fileservice"
}
resource "aws_subnet" "fileservice_public_subnet" {
  vpc_id            = aws_vpc.fileservice_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "fileservice_private_subnet" {
  vpc_id            = aws_vpc.fileservice_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_internet_gateway" "fileservice_igw" {
  vpc_id = aws_vpc.fileservice_vpc.id
}

resource "aws_nat_gateway" "fileservice_nat" {
  allocation_id = aws_eip.fileservice_eip.id
  subnet_id     = aws_subnet.fileservice_public_subnet.id
}

resource "aws_eip" "fileservice_eip" {
  vpc = true
}

resource "aws_route_table" "fileservice_public_rt" {
  vpc_id = aws_vpc.fileservice_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.fileservice_igw.id
  }
}

resource "aws_route_table_association" "fileservice_public_rt_assoc" {
  subnet_id      = aws_subnet.fileservice_public_subnet.id
  route_table_id = aws_route_table.fileservice_public_rt.id
}

resource "aws_route_table" "fileservice_private_rt" {
  vpc_id = aws_vpc.fileservice_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.fileservice_nat.id
  }
}

resource "aws_route_table_association" "fileservice_private_rt_assoc" {
  subnet_id      = aws_subnet.fileservice_private_subnet.id
  route_table_id = aws_route_table.fileservice_private_rt.id
}

resource "aws_security_group" "fileservice_security_group" {
  vpc_id = aws_vpc.fileservice_vpc.id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_cluster" "fileservice_cluster" {
  name = "fileservice-cluster"
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

resource "aws_ecs_task_definition" "fileservice_task" {
  family                   = "fileservice-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  container_definitions    = jsonencode([
    {
      name  = "fileservice-container"
      image = "${aws_ecr_repository.fileservice.repository_url}.amazonaws.com/fileservice:latest"
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
          "awslogs-group"        = "fileservice-log-group"
          "awslogs-region"       = "${var.aws_default_region}"
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
          name  = "AWS_CLOUDWATCH_LOGS_LOG_GROUP"
          value = var.aws_cloudwatch_logs_log_group
        },
        {
          name  = "AWS_DEFAULT_REGION"
          value = var.aws_default_region
        },
        {
          name  = "AWS_SECRET_ACCESS_KEY"
          value = var.aws_secret_access_key
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
    }
  ])
}

resource "aws_ecs_service" "fileservice_service" {
  name            = "fileservice-service"
  cluster         = aws_ecs_cluster.fileservice_cluster.id
  task_definition = aws_ecs_task_definition.fileservice_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = [aws_subnet.fileservice_private_subnet.id]
    security_groups = [aws_security_group.fileservice_security_group.id]
    assign_public_ip = true
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

variable "aws_cloudwatch_logs_log_group" {
  description = "AWS CloudWatch Logs Log Group"
  type        = string
}

variable "aws_default_region" {
  description = "AWS Default Region"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key"
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