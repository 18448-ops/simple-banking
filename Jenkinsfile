pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "manel/simple-banking-api"
        DOCKER_REGISTRY = "docker.io" // Si tu utilises Docker Hub, sinon, spécifie ton registre
    }

    stages {
        // Étape 1 : Cloner le code source depuis GitHub
        stage('Checkout') {
            steps {
                git 'https://github.com/18448-ops/simple-banking.git'
            }
        }

        // Étape 2 : Installer les dépendances
        stage('Install Dependencies') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'  // Exemple pour Python, ajuste selon ton environnement
                }
            }
        }

        // Étape 3 : Exécuter les tests unitaires
        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest tests/'  // Exécute les tests unitaires avec pytest
                }
            }
        }

        // Étape 4 : Construire l'image Docker
        stage('Build Docker image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        // Étape 5 : Exécuter un scan de sécurité avec Trivy
        stage('Scan Docker image with Trivy') {
            steps {
                script {
                    sh 'trivy image $DOCKER_IMAGE'  // Scanne l'image Docker pour des vulnérabilités
                }
            }
        }

        // Étape 6 : Exécuter le conteneur Docker en local (utile pour tests locaux)
        stage('Run Docker container locally') {
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

        // Étape 7 : Déployer sur Kubernetes (ajuster en fonction de ton setup Kubernetes)
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Déploie sur Kubernetes en utilisant kubectl et le fichier de déploiement YAML
                    sh 'kubectl apply -f k8s/deployment.yaml'
                }
            }
        }

        // Étape 8 : Envoi de rapports de tests ou de sécurité (optionnel)
        stage('Send Reports') {
            steps {
                script {
                    // Exemple pour envoyer un e-mail avec le rapport de tests
                    mail to: 'ton-email@exemple.com',
                         subject: "Rapport Jenkins - Build et Tests",
                         body: "Le pipeline Jenkins est terminé. Consultez les résultats."
                }
            }
        }
    }

    post {
        always {
            // Nettoyage des conteneurs Docker après l'exécution
            sh 'docker stop simple-banking-api || true'
            sh 'docker rm simple-banking-api || true'
        }

        success {
            echo "Pipeline terminé avec succès!"
        }

        failure {
            echo "Le pipeline a échoué, vérifier les logs pour plus de détails."
        }
    }
}
