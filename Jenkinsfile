pipeline {
    agent any

    stages {
        stage('Checkpoint for Build Trigger Message'){
            steps{
                script{
                    def lastCommitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    if (lastCommitMessage.contains('do-build')) {
                        echo"Build trigger keyword(do-build) found in commit message. Starting the build and other stages..."
                    }else{
                        error("Aborting the new build due to No build trigger.")
                    }
                }
            }
        }
        stage('Building Docker Image') {
            steps {
                script {
                    echo "Yayyy I am building now."
                    fullBranchName= env.GIT_BRANCH
					branchName = fullBranchName.split(':')[1]
                    echo "Branch Name is ${branchName}"
                }
            }
        }
    }
}
