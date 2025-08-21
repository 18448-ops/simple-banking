pipeline {
    agent any

    environment {
        // Définir l'URL du serveur SonarQube et le token d'authentification
        SONARQUBE_URL = 'http://192.168.189.138:9000' // Remplace par ton URL SonarQube
        SONARQUBE_TOKEN = credentials('sonarqube-token') // Le token que tu as configuré dans Jenkins
    }

    stages {
        // Étape de récupération du code source
        stage('Checkout') {
            steps {
                checkout scm // Récupère le code du repository GitHub
            }
        }

        // Étape de construction de l'image Docker
        stage('Build Docker Image') {
            steps {
                script {
                    // Construction de l'image Docker
                    sh 'docker build -t manel/simple-banking-api .'
                }
            }
        }

        // Étape d'analyse SonarQube
        stage('SonarQube Analysis') {
            steps {
                script {
                    // Exécution de l'analyse SonarQube avec le scanner Docker
                    sh """
                        docker run --rm \
                            -e SONARQUBE_URL=${SONARQUBE_URL} \
                            -e SONARQUBE_TOKEN=${SONARQUBE_TOKEN} \
                            sonarsource/sonar-scanner-cli
                    """
                }
            }
        }

        // Étape de déploiement du container Docker
        stage('Run Docker Container') {
            steps {
                script {
                    // Exécution du conteneur Docker en arrière-plan
                    sh 'docker run -d --name simple-banking-api manel/simple-banking-api'
                }
            }
        }
    }

    post {
        always {
            // Nettoyage après le pipeline, arrêter et supprimer le conteneur s'il existe
            sh 'docker stop simple-banking-api || true'
            sh 'docker rm simple-banking-api || true'
        }

        success {
            // Actions en cas de succès du pipeline
            echo 'Le pipeline a été exécuté avec succès.'
        }

        failure {
            // Actions en cas d'échec du pipeline
            echo 'Le pipeline a échoué. Vérifier les logs pour plus de détails.'
        }
    }
}
