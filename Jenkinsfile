pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Étape pour récupérer le code source depuis ton référentiel en utilisant SSH
                // Par exemple, en utilisant la commande git avec SSH
                sh 'git clone git@github.com:Xhakayoub/PythonApi_for_AIT.git'
            }
        }

     stage('Build') {
            steps {
                // Étape pour construire ton application Python
                // Par exemple, en utilisant un gestionnaire de paquets comme pip
                sh 'pip install -r requirements.txt'
                sh 'python setup.py build'
            }
        }
        
    stage('Test') {
            steps {
                // Étape pour exécuter les tests de ton application
                // Par exemple, en utilisant pytest
                sh 'pytest'
            }
        }

    stage('Deploy') {
            steps {
                // Étape pour déployer ton application Python
                // Par exemple, en utilisant un outil de déploiement comme Ansible ou en exécutant des commandes shell
                sh 'ansible-playbook deploy.yml'
                // Ou
                sh 'python deploy.py'
            }
        }
        
        // Les autres étapes du pipeline
        // ...
    }
}
