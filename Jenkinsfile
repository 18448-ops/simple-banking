pipeline {
    agent any

    environment {
        // Utilisation de SonarQube local
        SONARQUBE_URL = 'http://192.168.189.138:9000'
        SONARQUBE_TOKEN = credentials('sonarqube-token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t manel/simple-banking-api .'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    sh """
                        # Créer un fichier sonar-scanner.properties
                        echo "sonar.host.url=${SONARQUBE_URL}" > sonar-scanner.properties
                        echo "sonar.login=${SONARQUBE_TOKEN}" >> sonar-scanner.properties

                        # Exécuter SonarScanner avec les propriétés configurées
                        docker run --rm \
                            -v ${PWD}/sonar-scanner.properties:/opt/sonar-scanner/conf/sonar-scanner.properties \
                            sonarsource/sonar-scanner-cli
                    """
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker run -d --name simple-banking-api manel/simple-banking-api'
                }
            }
        }
    }

    post {
        always {
            sh 'docker stop simple-banking-api || true'
            sh 'docker rm simple-banking-api || true'
        }

        success {
            echo 'Le pipeline a été exécuté avec succès.'
        }

        failure {
            echo 'Le pipeline a échoué. Vérifier les logs pour plus de détails.'
        }
    }
}
