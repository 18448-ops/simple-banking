pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "manel/simple-banking-api"
        SONARQUBE_SERVER = "SonarQube-Server"  // Nom du serveur SonarQube configuré
    }

    stages {
        stage('Checkout') {
            steps {
                // Utilisation de credentials pour GitHub
                git branch: 'main', url: 'https://github.com/18448-ops/simple-banking.git', credentialsId: 'github-credentials'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Construction de l'image Docker
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // Analyse SonarQube dans un bloc avecSonarQubeEnv
                withSonarQubeEnv('SonarQube-Server') {  // Utilise le nom du serveur SonarQube configuré dans Jenkins
                    sh 'mvn clean install sonar:sonar -Dsonar.projectKey=your_project_key'
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run -d --name simple-banking-api -p 8000:8000 $DOCKER_IMAGE'
                // Ajouter ici les étapes pour exécuter les tests
            }
        }
    }

    post {
        always {
            cleanWs() // Nettoyage de l'espace de travail
        }

        success {
            echo "Pipeline executed successfully"
        }

        failure {
            echo "Pipeline failed"
        }
    }
}
