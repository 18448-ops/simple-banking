pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "manel/simple-banking-api"
        SONARQUBE = 'SonarQube-Server'  // Nom de ton serveur SonarQube configuré
        KUBERNETES_NAMESPACE = 'default' // Namespace Kubernetes où déployer l'application
    }

    stages {
        // Étape 1 : Cloner le code source depuis GitHub
        stage('Clone repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/18448-ops/simple-banking.git',
                    credentialsId: 'github-credentials'
            }
        }

        // Étape 2 : Vérifier Docker avant de continuer
        stage('Verify Docker Installation') {
            steps {
                script {
                    sh 'which docker'  // Affiche le chemin de Docker
                    sh 'docker --version'  // Affiche la version de Docker
                }
            }
        }

        // Étape 3 : Analyser le code avec SonarQube
        stage('SonarQube Analysis') {
            steps {
                script {
                    sh ''' 
                    mvn sonar:sonar \
                    -Dsonar.projectKey=simple-banking-api \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=${SONARQUBE_TOKEN}
                    '''
                }
            }
        }

        // Étape 4 : Construire l'image Docker
        stage('Build Docker image') {
            steps {
                script {
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                }
            }
        }

        // Étape 5 : Scanner l'image Docker avec Trivy
        stage('Trivy Scan') {
            steps {
                script {
                    sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL ${DOCKER_IMAGE}'
                }
            }
        }

        // Étape 6 : Exécuter le conteneur Docker
        stage('Run Docker container') {
            steps {
                script {
                    sh '''
                    docker stop simple-banking-api || true
                    docker rm simple-banking-api || true
                    docker run -d --name simple-banking-api -p 8000:8000 ${DOCKER_IMAGE}
                    '''
                }
            }
        }

        // Étape 7 : Déployer l'application dans Kubernetes
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh '''
                    kubectl apply -f k8s/deployment.yml --namespace=${KUBERNETES_NAMESPACE}
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
