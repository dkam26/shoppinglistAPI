pipeline {
    agent any
    
    
    stages {
        stage('build') {
            steps {
                echo 'cloning github repository'
                sh ' rm -r shoppinglistAPI'
                sh 'git clone https://github.com/dkam26/shoppinglistAPI.git/'
                sh 'virtualenv venv'
                sh 'ls'
                sh '. venv/bin/activate'
                sh 'pip install -r shoppinglistAPI/requirements.txt'
                
            }
        }
        
        stage('Test'){
            steps{
                echo 'Run tests'
                sh 'ls'
                
                sh 'nosetests shoppinglistAPI/tests  --with-coverage --cover-package=shoppinglistAPI/my_app'
                
            }
        }
    }

}
