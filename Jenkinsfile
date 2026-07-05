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
                url: 'https://github.com/kathan-10/flask-weather.git'
            }
        }

        stage('Build Docker Image') {

            steps {

                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
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

        stage('Update Deployment File') {

            steps {

                sh '''
                sed -i "s|image:.*|image: $IMAGE_NAME:$IMAGE_TAG|g" deployment.yml
                '''
            }
        }

        stage('Deploy Kubernetes') {

            steps {

                sh '''
                
		kubectl apply -f secret.yml

		kubectl apply -f deployment.yml

                kubectl apply -f service.yml

                kubectl rollout restart deployment flask-weather
                '''
            }
        }
    }
}
