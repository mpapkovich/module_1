pipeline {
  agent { docker { image 'python:3.8.2' } }
  stages {
   
    stage('Build') {
      steps {
        sh 'python main.py'
      }
    }
 stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}


