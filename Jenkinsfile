pipeline {
    agent any

    stages {
        stage('Check for Build Trigger Message'){
            steps{
                script{
                    def lastCommitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    if (lastCommitMessage.contains('#build-trigger')) {
                        echo"Build trigger keyword/comment found in commit message. Starting the build and other stages..."
                    }else{
                        error("Aborting the new build")
                    }
                }
            }
        }
        stage{
            when { expression { lastCommitMessage.contains('#build-trigger') } }
            steps('Building Docker Image'){
                script{
                    echo"Yayyy I am building now."
                }
            }
        }
    }
}
