pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "manel/simple-banking-api"
    }

    stages {
        stage('Build Docker image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Run Docker container') {
            steps {
                script {
                    sh '''
                    docker stop simple-banking-api || true
                    docker rm simple-banking-api || true
                    docker run -d --name simple-banking-api -p 8000:8000 $DOCKER_IMAGE
                    '''
                }
            }
        }
    }
}
