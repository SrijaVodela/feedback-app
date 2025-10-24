pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "srijavodela/feedback-app"
        DOCKER_USER = "srijavodela"
        DOCKER_PASS = "Srija1@Praneetha"
        // Ensure you have added this path in Jenkins Global Properties
        KUBECONFIG = "C:\\Users\\Srija\\.kube\\config"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Pulling code from GitHub..."
                git branch: 'main', url: 'https://github.com/SrijaVodela/feedback-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t %DOCKER_IMAGE%:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "Logging in to Docker Hub and pushing image..."
                bat """
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker push %DOCKER_IMAGE%:latest
                """
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying application to Kubernetes..."
                bat "kubectl apply -f deployment.yaml"
                bat "kubectl apply -f service.yaml"
                bat "kubectl get pods"  // Optional, verify deployment
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Build or deployment failed."
        }
    }
}
