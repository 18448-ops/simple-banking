pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://192.168.189.138:9000' // URL de SonarQube
        SONARQUBE_TOKEN = credentials('sonarqube-token') // Utilisation du token SonarQube stocké dans Jenkins
        DATABASE_URL = "postgresql://user:password@192.168.189.135/mydb"  // Connexion à PostgreSQL sur une machine distante
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

        stage('Install dependencies') {
            steps {
                script {
                    echo 'Installing python3-venv package...'
                    sh '''
                        sudo apt-get update
                        sudo apt-get install -y python3.11-venv
                    '''
                    echo 'Creating virtual environment and installing dependencies...'
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh '''
                        . venv/bin/activate
                        export DATABASE_URL="${DATABASE_URL}"
                        pytest --maxfail=1 --disable-warnings -q
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    echo 'Running SonarQube analysis...'
                    withSonarQubeEnv('sonarqube') {
                        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                            sh '''
                                ${tool 'sonar-scanner'}/bin/sonar-scanner \
                                  -Dsonar.projectKey=simple-banking \
                                  -Dsonar.sources=src \
                                  -Dsonar.host.url=$SONARQUBE_URL \
                                  -Dsonar.login=$SONAR_TOKEN
                            '''
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t simple-banking-api .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    echo 'Running the Docker container...'
                    sh 'docker run -d --name simple-banking-api simple-banking-api'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh '''
                docker stop simple-banking-api || true
                docker rm simple-banking-api || true
            '''
        }
        failure {
            echo 'The pipeline failed. Please check the logs for details.'
        }
    }
}
