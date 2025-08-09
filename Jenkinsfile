pipeline {
    agent none  // Pas d'agent par défaut, chaque étape aura un agent spécifique

    tools {
        maven 'Maven 3'  // Utilise l'installation de Maven nommée 'Maven 3' définie dans Jenkins
    }

    environment {
        GIT_REPO = 'https://github.com/18448-ops/simple-banking.git'
        BRANCH = 'main'  // Ou un autre nom de branche selon ton besoin
    }

    stages {
        // Étape de récupération du code source depuis Git
        stage('Checkout') {
            agent { node { label 'built-in' } }
            steps {
                checkout scm  // Vérifie le code source depuis Git
                script {
                    // Vérifie que le bon dépôt et la bonne branche sont utilisés
                    echo "Cloning repository from ${env.GIT_REPO} branch ${env.BRANCH}"
                }
            }
        }

        // Étape de build Docker
        stage('Build Docker Image') {
            agent { node { label 'built-in' } }
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t manel/simple-banking-api .'  // Construction de l'image Docker
                }
            }
        }

        // Étape d'analyse de sécurité avec Trivy
        stage('Trivy Scan') {
            agent { node { label 'built-in' } }
            steps {
                script {
                    echo 'Running Trivy scan...'
                    sh 'trivy image --format json --output trivy_report.json manel/simple-banking-api'  // Scanner avec Trivy
                }
            }
        }

        // Étape d'analyse de qualité de code avec SonarQube
        stage('SonarQube Analysis') {
            agent { node { label 'built-in' } }
            steps {
                script {
                    echo 'Running SonarQube analysis...'
                    withSonarQubeEnv('SonarQube-Server') {
                        sh 'mvn clean install sonar:sonar -Dsonar.projectKey=your_project_key'  // Analyse SonarQube avec Maven
                    }
                }
            }
        }

        // Étape de tests (unitaires, etc.)
        stage('Run Tests') {
            agent { node { label 'built-in' } }
            steps {
                script {
                    echo 'Running tests...'
                    // Exemple de commande pour exécuter les tests, adapte selon ton besoin
                    sh 'pytest tests/'  // Exécution des tests avec pytest
                }
            }
        }

        // Étape de nettoyage (post-actions)
        stage('Post Actions') {
            agent { node { label 'built-in' } }
            steps {
                script {
                    cleanWs()  // Nettoie l'espace de travail après l'exécution du pipeline
                    echo 'Workspace cleaned.'
                }
            }
        }
    }
}
