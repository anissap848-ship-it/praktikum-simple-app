pipeline {
    agent any
    environment {
        IMAGE_NAME = 'anissaauliyaputri/simple-app'
        REGISTRY = 'https://index.docker.io/v1/'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Melakukan checkout dari SCM...'
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Mulai build aplikasi'
                echo 'Build selesai'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Membangun Docker image...'
                    docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
                    echo "Image berhasil dibuat: ${IMAGE_NAME}:${env.BUILD_NUMBER}"
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Push image ke Docker Hub...'
                    docker.withRegistry(REGISTRY, REGISTRY_CREDENTIALS) {
                        docker.image("${IMAGE_NAME}:${env.BUILD_NUMBER}").push()
                        docker.image("${IMAGE_NAME}:${env.BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }
        stage('Deploy (App + MySQL)') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker compose up -d'
                    } else {
                        bat 'docker compose up -d'
                    }
                }
            }
        }
        stage('Verify') {
            steps {
                sleep time: 20, unit: 'SECONDS'
                retry(5) {
                    script {
                        def check = 'docker exec praktikum-app python -c "import urllib.request; print(urllib.request.urlopen(\'http://localhost:5000/health\').read().decode())"'
                        if (isUnix()) { sh check } else { bat check }
                    }
                    sleep time: 5, unit: 'SECONDS'
                }
            }
        }
    }
    post {
        always {
            echo 'Selesai build'
        }
    }
}