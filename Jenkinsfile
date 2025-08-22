pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://192.168.189.138:9000'  // L'URL de ton serveur SonarQube
        SONARQUBE_TOKEN = credentials('sonarqube-token') // Utilisation de 'sonarqube-token' pour l'authentification à SonarQube
    }

    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    echo 'Checking out the source code from the repository...'
                    checkout scm
                }
            }
        }

        stage('Install python3-venv') {
            steps {
                script {
                    echo 'Installing python3-venv package...'
                    sh 'sudo apt-get update && sudo apt-get install -y python3-venv'
                }
            }
        }

        stage('Build') {
            steps {
                echo "Création de la virtualenv et installation des dépendances..."
                sh """
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                echo "Exécution des tests..."
                sh """
                    . ${VENV_DIR}/bin/activate
                    export DATABASE_URL="$DATABASE_URL"
                    export PYTHONPATH="$PYTHONPATH"
                    pytest --maxfail=1 --disable-warnings -q
                """
            }
        }

        stage('Analyse SAST avec SonarQube') {
            when { expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } }
            steps {
                echo "Analyse SAST avec SonarQube..."
                withSonarQubeEnv('sonarqube') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh """
                            ${tool 'sonar-scanner'}/bin/sonar-scanner \
                              -Dsonar.projectKey=simple-banking \
                              -Dsonar.sources=src \
                              -Dsonar.host.url=$SONAR_HOST_URL \
                              -Dsonar.login=$SONAR_TOKEN
                        """
                    }
                }
            }
        }
    }

    post {
        always { echo "Pipeline terminé" }
        success { echo "✅ Pipeline réussi" }
        failure { echo "❌ Pipeline échoué" }
    }
}
