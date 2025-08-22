pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://192.168.189.138:9000' // URL de SonarQube
        SONARQUBE_TOKEN = credentials('sonarqube-token') // Utilisation du token SonarQube stocké dans Jenkins
        DATABASE_URL = "postgresql://user:password@192.168.189.135/mydb"  // Connexion à PostgreSQL sur une machine distante
        DOCKER_IMAGE = "manel/simple-banking-api"  // Image Docker à construire
    }

    stages {
        // Étape 1 : Cloner le code source depuis GitHub (branche main)
        stage('Clone repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/18448-ops/simple-banking.git', 
                    credentialsId: 'github-credentials'
            }
        }

        // Étape 2 : Installer les dépendances et créer un environnement virtuel
        stage('Install dependencies') {
            steps {
                script {
                    echo 'Installing python3-venv package...'
                    sh '''
                        # Installation des dépendances sans sudo si déjà installé sur l'agent
                        apt-get update || true
                        apt-get install -y python3.11-venv || true
                    '''
                    echo 'Creating virtual environment and installing dependencies...'
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        // Étape 3 : Lancer les tests
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh '''
                        . venv/bin/activate
                        export DATABASE_URL="${DATABASE_URL}"
                        pytest --maxfail=1 --disable-warnings -q
                    '''
                }
            }
        }

        // Étape 4 : Analyser le code avec SonarQube
        stage('SonarQube Analysis') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    echo 'Running SonarQube analysis...'
                    withSonarQubeEnv('sonarqube') {
                        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                            sh '''
                                ${tool 'sonar-scanner'}/bin/sonar-scanner \
                                  -Dsonar.projectKey=simple-banking \
                                  -Dsonar.sources=src \
                                  -Dsonar.host.url=$SONARQUBE_URL \
                                  -Dsonar.login=$SONAR_TOKEN
                            '''
                        }
                    }
                }
            }
        }

        // Étape 5 : Construire l'image Docker
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        // Étape 6 : Exécuter le conteneur Docker
        stage('Run Docker Container') {
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
