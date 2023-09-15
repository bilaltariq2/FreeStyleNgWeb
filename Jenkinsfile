pipeline {
    agent any

    stages {
        stage('Check for Build Trigger Message'){
            steps{
                script{
                    def lastCommitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    echo "Message: ${lastCommitMessage}"
                    echo "GIT_COMMIT ${GIT_COMMIT}"
                    echo "GIT_PREVIOUS_COMMIT ${GIT_PREVIOUS_COMMIT}"
                    echo "GIT_PREVIOUS_SUCCESSFUL_COMMIT ${GIT_PREVIOUS_SUCCESSFUL_COMMIT}"

                }
            }
        }
    }
}
