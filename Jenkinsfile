pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "manel/simple-banking-api"
    }

    stages {
        // Étape 1 : Cloner le code source depuis GitHub
        stage('Clone repo') {
            steps {
                git url: 'https://github.com/18448-ops/simple-banking.git', credentialsId: 'github-credentials'
            }
        }

        // Étape 2 : Construire l'image Docker
        stage('Build Docker image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        // Étape 3 : Exécuter le conteneur Docker
        stage('Run Docker container') {
            steps {
                script {
                    // Arrêter et supprimer le conteneur existant (si présent)
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
            // Nettoyer après l'exécution, au cas où le conteneur n'est pas arrêté correctement
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

