pipeline {
    agent any
    environment {
        SONARQUBE_SERVER = 'SonarQube-Server' // Le nom du serveur SonarQube configuré dans Jenkins
        MAVEN_HOME = tool name: 'Maven 3', type: 'Maven'  // Assurez-vous que Maven est installé dans Jenkins
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
                    // Si vous avez des tests unitaires, vous pouvez les exécuter ici
                    sh 'pytest'  // Exemple pour Python, adaptez en fonction de votre projet
                }
            }
        }

        stage('Post Actions') {
            steps {
                cleanWs()
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
