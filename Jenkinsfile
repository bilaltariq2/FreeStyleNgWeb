pipeline{
	agent any
	environment{
		registry="055638961298.dkr.ecr.us-east-1.amazonaws.com/"
		repoName="rashid/test"
		dockerImage = ''
		imageTag = ''
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
						def branchName = env.GIT_BRANCH.split('/')[1]
						imageTag = "${branchName}-143" 
                    }
                }
            }
        }
		stage{
			steps{
				script{
					echo "Image tag is ${imageTag}"
				}
			}
		}
	}

}
