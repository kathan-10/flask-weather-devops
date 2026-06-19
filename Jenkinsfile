pipeline {

    agent any

    environment {

        IMAGE_NAME = "kathan1205/flask-weather"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Clone Code') {

            steps {
                git branch: 'main',
                url: 'YOUR_GITHUB_REPO'
            }
        }

        stage('Build Docker Image') {

            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push Docker Image') {

            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'docker',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                    docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Update Deployment') {

            steps {

                sh '''
                sed -i "s|image:.*|image: $IMAGE_NAME:$IMAGE_TAG|g" deployment.yaml
                '''
            }
        }

        stage('Deploy Kubernetes') {

            steps {

                sh '''
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                '''
            }
        }
    }
}
