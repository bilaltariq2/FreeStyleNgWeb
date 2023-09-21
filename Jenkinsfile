pipeline{
	agent any
	environment{
		registry="055638961298.dkr.ecr.us-east-1.amazonaws.com/"
		repoName="rashid/test"
		dockerImage = ''
		imageTag = ''
		imageDigest = ''
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
		stage('Fetching Image Digest & Generating PDF Report'){
			steps{
				script{
					imageDigest = sh(script: "aws ecr describe-images --repository-name ${repoName} --image-ids imageTag=${imageTag} --query 'imageDetails[0].imageDigest' --output text", returnStdout: true).trim()
					//scannedData = sh(script: "aws ecr describe-image-scan-findings --repository-name ${repoName} --image-id imageDigest=${imageDigest}", returnStdout: true).trim()
					sh "aws ecr describe-image-scan-findings --repository-name ${repoName} --image-id imageDigest=${imageDigest} >> scanData.txt"
					sh "python3 main.py"
					sh "email.sh"
				}
			}
		}
	}
}
