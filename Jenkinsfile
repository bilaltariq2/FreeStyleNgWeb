pipeline{
	agent any
	environment{
		registry="btariq/jenkins-learning"
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
		stage('Logging in to AWS'){
			steps{
				script{
					sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 055638961298.dkr.ecr.us-east-1.amazonaws.com"
				}
			}
		}
	}
}
