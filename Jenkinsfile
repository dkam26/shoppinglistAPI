pipeline {
    agent any
    
    
    stages {
        stage('build') {
            steps {
                echo 'cloning github repository'
                
                git branch: 'develop', url: 'https://github.com/dkam26/shoppinglistAPI.git'
                sh 'virtualenv venv'
                sh 'ls'
                sh '. venv/bin/activate'
                sh ' pip install --user -r requirements.txt'
                
            }
        }
        
        stage('Test'){
            steps{
                echo 'Run tests'
                sh 'ls'
                
                sh 'nosetests tests  --with-coverage --cover-package=my_app'
                
            }
        }
    }

}

