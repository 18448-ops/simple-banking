pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "manel/simple-banking-api"
        SONARQUBE_URL = "http://192.168.189.138:9000" // L'IP de VM2 (SonarQube)
        SONARQUBE_TOKEN = credentials('sonarqube-token') // Token SonarQube enregistré dans Jenkins
        TRIVY_IMAGE = "manel/simple-banking-api" // Image Docker pour le scan Trivy
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

        // Étape 2 : Construire l'image Docker
        stage('Build Docker image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        // Étape 3 : Scanner l'image Docker avec Trivy pour les vulnérabilités
        stage('Trivy Scan') {
            steps {
                script {
                    echo "Starting Trivy scan..."
                    sh "trivy image --exit-code 1 --severity HIGH,CRITICAL --no-progress --format table $DOCKER_IMAGE"
                }
            }
        }

        // Étape 4 : Analyse du code avec SonarQube
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo "Starting SonarQube analysis..."
                    withSonarQubeEnv('SonarQube') { // Assurez-vous d'avoir configuré l'outil SonarQube dans Jenkins
                        sh "mvn clean verify sonar:sonar -Dsonar.projectKey=simple-banking-api -Dsonar.host.url=$SONARQUBE_URL -Dsonar.login=$SONARQUBE_TOKEN"
                    }
                }
            }
        }

        // Étape 5 : Exécuter le conteneur Docker (uniquement si le scan Trivy est réussi)
        stage('Run Docker container') {
            when {
                expression {
                    return currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                script {
                    echo "Running Docker container..."
                    sh '''
                    docker stop simple-banking-api || true
                    docker rm simple-banking-api || true
                    docker run -d --name simple-banking-api -p 8000:8000 $DOCKER_IMAGE
                    '''
                }
            }
        }

        // Étape 6 : Tests unitaires (exemple de test ici avec pytest)
        stage('Unit Tests') {
            steps {
                script {
                    echo "Running unit tests..."
                    sh 'pytest tests/'
                }
            }
        }
    }

    post {
        always {
            // Nettoyage des ressources Docker
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
