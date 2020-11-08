pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('build') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'python -m py_compile module_1/main.py '
        stash(name: 'compiled-results', includes: 'module_1/*.py*')
      }
    }
  }
}

