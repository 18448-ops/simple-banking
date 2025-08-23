pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        PYTHONPATH = "${WORKSPACE}/src"
        PIP_CACHE_DIR = "${WORKSPACE}/.pip-cache"
        ENVIRONMENT = "test" // test pour SQLite, dev/prod pour PostgreSQL
        DATABASE_URL = "${env.ENVIRONMENT == 'test' ? 'sqlite:///./test_banking.db' : (env.DATABASE_URL ?: 'postgresql://user:password@192.168.189.135/mydb')}"
        SONARQUBE_URL = 'http://192.168.189.138:9000'  // URL de SonarQube
        SONARQUBE_TOKEN = credentials('sonarqube-token')  // Utilisation du token SonarQube stocké dans Jenkins
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo "Clonage du code source..."
                checkout scm
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
                              -Dsonar.host.url=$SONARQUBE_URL \
                              -Dsonar.login=$SONAR_TOKEN
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Construction de l'image Docker..."
                sh """
                    docker build -t simple-banking-api .
                """
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Exécution du conteneur Docker..."
                sh """
                    docker stop simple-banking-api || true
                    docker rm simple-banking-api || true
                    docker run -d --name simple-banking-api -p 8000:8000 simple-banking-api
                """
            }
        }
    }

    post {
        always {
            echo "Nettoyage et arrêt des conteneurs..."
            sh '''
                docker stop simple-banking-api || true
                docker rm simple-banking-api || true
            '''
        }
        success {
            echo "✅ Pipeline réussi"
        }
        failure {
            echo "❌ Pipeline échoué"
        }
    }
}
