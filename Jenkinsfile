pipeline {
    agent any

    stages {
        stage('Check for Build Trigger Message'){
            steps{
                script{
                    def lastCommitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    if (lastCommitMessage.contains('do-build')) {
                        echo"Build trigger keyword/comment found in commit message. Starting the build and other stages..."
                    }else{
                        error("Aborting the new build due to No build trigger.")
                    }
                }
            }
        }
        stage('Building Docker Image') {
            // when {
            //     expression { lastCommitMessage.contains('do-build') }
            // }
            steps {
                script {
                    echo "Yayyy I am building now."
                }
            }
        }
    }
}
