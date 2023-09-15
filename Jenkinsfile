pipeline {
    agent any

    stages {
        stage('Check for Build Trigger Message'){
            steps{
                script{
                    def lastCommitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    echo "Message: ${lastCommitMessage}"
                }
            }
        }
    }
}
