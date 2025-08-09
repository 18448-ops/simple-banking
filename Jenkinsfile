pipeline {
    agent any // Utiliser un agent par défaut, ou remplace par 'node("label")' si tu as un label spécifique

    tools {
        maven 'Maven 3' // Nom de l'installation Maven dans Jenkins (doit correspondre à la configuration)
    }

    environment {
        SONARQUBE_SERVER = 'SonarQube-Server' // Nom de la configuration SonarQube dans Jenkins
        MAVEN_HOME = tool name: 'Maven 3', type: 'Maven' // Assure-toi que Maven est bien installé et configuré
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
                    // Construire l'image Docker
                    sh 'docker build -t manel/simple-banking-api .'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Exécuter l'analyse SonarQube avec Maven
                    withSonarQubeEnv(SONARQUBE_SERVER) {
                        sh "${MAVEN_HOME}/bin/mvn clean install sonar:sonar -Dsonar.projectKey=your_project_key"
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Exécuter les tests unitaires si nécessaire
                    sh 'pytest' // Exemple pour Python, adapte selon tes besoins
                }
            }
        }

        stage('Post Actions') {
            steps {
                node {
                    cleanWs() // Assurer que cleanWs est à l'intérieur du bloc node
                }
            }
        }
    }

    post {
        always {
            // Toujours effectuer un nettoyage après le pipeline
            cleanWs()
        }

        success {
            // Actions en cas de succès, comme envoyer une notification
            echo 'Pipeline completed successfully!'
        }

        failure {
            // Actions en cas d'échec, comme envoyer un email de notification
            echo 'Pipeline failed!'
        }
    }
}
