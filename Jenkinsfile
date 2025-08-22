pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://192.168.189.138:9000'  // L'URL de ton serveur SonarQube
        SONARQUBE_TOKEN = credentials('sonarqube-token') // Utilisation de 'sonarqube-token' pour l'authentification à SonarQube
        POSTGRES_USER = credentials('postgres-username')  // Nom d'utilisateur de la base PostgreSQL
        POSTGRES_PASSWORD = credentials('postgres-password')  // Mot de passe de la base PostgreSQL
        POSTGRES_DB = 'mydb'  // Base de données PostgreSQL
    }

    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    echo 'Checking out the source code from the repository...'
                    checkout scm
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image for the application...'
                    sh '''
                        docker build -t simple-banking-api .
                    '''
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    echo 'Running the Docker container...'
                    sh '''
                        docker run -d --name simple-banking-api \
                        -e DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost/$POSTGRES_DB \
                        simple-banking-api
                    '''
                }
            }
        }

        stage('Install python3-venv') {
            steps {
                script {
                    echo 'Installing python3-venv package inside the container...'
                    sh '''
                        apt-get update && apt-get install -y python3-venv
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                echo "Running unit tests..."
                sh '''
                    docker exec simple-banking-api pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    echo 'Running SonarQube analysis...'
                    sh '''
                        docker run --rm \
                            -v ${WORKSPACE}/sonar-scanner.properties:/opt/sonar-scanner/conf/sonar-scanner.properties \
                            -e SONARQUBE_URL=${SONARQUBE_URL} \
                            -e SONARQUBE_TOKEN=${SONARQUBE_TOKEN} \
                            sonarsource/sonar-scanner-cli
                    '''
                }
            }
        }

        stage('Post Actions') {
            steps {
                echo 'Cleaning up...'
                sh '''
                    docker stop simple-banking-api || true
                    docker rm simple-banking-api || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo '✅ Pipeline completed successfully.'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
