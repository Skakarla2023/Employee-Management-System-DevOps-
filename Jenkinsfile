pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
    steps {
        sh '. .venv/bin/activate && python -m pytest -q'
    }
}

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t employee-management:latest .'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker compose up -d --build'
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
    }
}
