pipeline {
    agent any

    environment {
        // Utilisation du token de SonarQube de Jenkins
        SONARQUBE_URL = 'http://192.168.189.138:9000' // Modifie ici si nécessaire
        SONARQUBE_TOKEN = credentials('sonarqube-token') // Assure-toi que l'id 'sonarqube-token' correspond bien à celui dans Jenkins
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
                        docker run --rm \
                            -v ${PWD}/sonar-scanner.properties:/opt/sonar-scanner/conf/sonar-scanner.properties \
                            -e SONARQUBE_URL=${SONARQUBE_URL} \
                            -e SONARQUBE_TOKEN=${SONARQUBE_TOKEN} \
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
            echo 'Le pipeline a éc
