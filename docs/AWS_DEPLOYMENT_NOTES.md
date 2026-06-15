# AWS Deployment Notes

## Region

Start with one AWS region, for example:

```text
us-west-2
```

Bedrock model availability varies by region, so verify model access in the chosen region before deployment.

## Required AWS pieces

- ECR repository for backend image
- ECS cluster
- ECS Fargate task definition
- ECS service
- Application Load Balancer
- IAM task execution role
- IAM task role
- CloudWatch log group

## IAM

The ECS task role needs permission to invoke Bedrock models.

Simple development policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    }
  ]
}
```

Later, restrict this to specific model ARNs.

## Bedrock model access

Some models require explicit access enablement in the Bedrock console.

Check:

```text
Amazon Bedrock Console
  -> Model access
  -> Enable desired models
```

## Environment variables

The ECS task should include:

```text
AWS_REGION
BEDROCK_DEFAULT_MODEL
APP_ENV
CORS_ORIGINS
```

Do not put AWS access keys into ECS environment variables. Use IAM roles.

## Frontend deployment choices

For learning, the simplest choices are:

1. Serve built React assets from FastAPI.
2. Deploy frontend to S3 + CloudFront.
3. Use AWS Amplify.

Do not overbuild the frontend deployment at first.
