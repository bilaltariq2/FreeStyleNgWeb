pipeline{
	agent any
	environment{
		registry="055638961298.dkr.ecr.us-east-1.amazonaws.com/"
		repoName="rashid/test"
		dockerImage = ''
		branchName = ''
	}

	stages{
		stage('Checkpoint for Build Trigger Message'){
            steps{
                script{
                    def lastCommitMessage = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                    if (lastCommitMessage.contains('No-build')) {
                        error("Aborting the new build due to No Build Message.")
                    }else{
                        echo"Starting the build and other stages..."                        
                    }
                }
            }
        }
		stage('Building Docker Image'){
			steps{
				script{
					branchName = env.GIT_BRANCH.split('/')[1]
					dockerImage = docker.build registry +"${repoName}:${branchName}-${BUILD_NUMBER}"
				}
			}
		}
		stage('Configure Amazon AWS CLI'){
			steps{
				script{
					docker.withRegistry('https://055638961298.dkr.ecr.us-east-1.amazonaws.com', 'ecr:us-east-1:aws_credentials') {
						sh "aws ecr list-images --repository-name rashid/test"
                        dockerImage.push()
                    }
				}
			}
		}
	}
}
