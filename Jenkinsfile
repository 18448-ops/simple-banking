pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "manel/simple-banking-api"
    }

    stages {
        stage('Clone repo') {
            steps {
                git url: 'https://github.com/ton-utilisateur/simple-banking.git', branch: 'main'
            }
        }

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
