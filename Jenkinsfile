pipeline {
    agent any

    stages {
        stage('Checkpoint for Build Trigger Message'){
            steps{
                script{
                    def lastCommitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    if (lastCommitMessage.contains('No-build')) {
                        error("Aborting the new build due to No build trigger.")
                    }else{
                        echo"Build trigger keyword(do-build) found in commit message. Starting the build and other stages..."                        
                    }
                }
            }
        }
        stage('Building Docker Image') {
            steps {
                script {
                    echo "I am building now."
					branchName = env.GIT_BRANCH.split('/')[1]
                    echo "Branch Name is ${branchName}"
                }
            }
        }
    }
}
