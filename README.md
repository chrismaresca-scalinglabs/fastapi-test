# Project Name

### Introduction

This project is a FastAPI application containerized with Docker. Before running the application, you need to create a `.env` file locally and set the necessary environment variables.

### Prerequisites

- Docker installed on your machine
- AWS account with access to Cognito

### Setup Instructions

1. **Clone the Repository**

```sh
git clone https://github.com/your-repo/project-name.git
cd project-name
```

2. **Create a .env File**

In the root directory of the project, create a file named .env. This file will contain the environment variables required for the application to function properly.

sh Copy code touch .env Add Environment Variables

Open the .env file in a text editor and add the following environment variables:

```sh
COGNITO_REGION=your_cognito_region
COGNITO_USER_POOL_ID=your_cognito_user_pool_id
COGNITO_APP_CLIENT_ID=your_cognito_app_client_id
```

Replace the placeholder values with your actual AWS Cognito configurations.

### Where to Find the Environment Variables

1. **COGNITO_REGION**:

The region can be found in the top right corner of the AWS Management Console after you log in.

2. **COGNITO_USER_POOL_ID**:

Navigate to the Amazon Cognito Dashboard. Click on "Manage User Pools". Select your user pool from the list. The User Pool ID will be displayed at the top of the "General settings" tab.

3. **COGNITO_APP_CLIENT_ID**:

In the same User Pool dashboard, click on "App integration" from the left-hand menu. Under the "App clients and analytics" section, you will find the App Client ID.

### Running the Application

After setting up your .env file, you can build and run the Docker container:

1. **Build the Docker Image:**

sh`docker build -t my-fastapi-app . `

Run the Docker Container:

sh`docker run --env-file .env -p 80:80 my-fastapi-app `

### Conclusion

Your FastAPI application should now be running, configured with your AWS Cognito credentials. Ensure that your .env file is not included in your version control by adding it to your .gitignore file.
