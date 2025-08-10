pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "manel/simple-banking-api"
        SONARQUBE_URL = "http://192.168.189.138:9000"
        SONARQUBE_TOKEN = "3rINM1HkWDD/nb7HmKbJYMVHZniCbwkC5xGCEp0AZTU="
    }

    stages {
        // Étape 1 : Cloner le code source depuis GitHub (branche Test-Sonarqube)
        stage('Clone repo') {
            steps {
                git branch: 'Test-Sonarqube', 
                    url: 'https://github.com/18448-ops/simple-banking.git', 
                    credentialsId: 'github-credentials'
            }
        }

        // Étape 2 : Vérifier la version de Docker
        stage('Docker Test') {
            steps {
                script {
                    sh 'docker --version'
                }
            }
        }

        // Étape 3 : Construire l'image Docker
        stage('Build Docker image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        // Étape 4 : Analyser le code avec SonarQube
        stage('SonarQube Analysis') {
            steps {
                script {
                    // Analyse du code source avec SonarQube pour la branche Test-sonarqube
                    sh """
                    sonar-scanner \
                    -Dsonar.projectKey=simple-banking-api \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=$SONARQUBE_URL \
                    -Dsonar.login=$SONARQUBE_TOKEN
                    """
                }
            }
        }

        // Étape 5 : Exécuter le conteneur Docker
        stage('Run Docker container') {
            steps {
                script {
                    // Arrêter et supprimer le conteneur existant (si présent), puis lancer le nouveau
                    sh '''
                    docker stop simple-banking-api || true
                    docker rm simple-banking-api || true
                    docker run -d --name simple-banking-api -p 8000:8000 $DOCKER_IMAGE
                    '''
                }
            }
        }
    }

    post {
        always {
            // Nettoyage du conteneur à la fin
            sh 'docker stop simple-banking-api || true'
            sh 'docker rm simple-banking-api || true'
        }

        success {
            echo "Le pipeline a réussi!"
        }

        failure {
            echo "Le pipeline a échoué, vérifier les logs pour plus de détails."
        }
    }
}
