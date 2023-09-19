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
		// stage('Building Docker Image'){
		// 	steps{
		// 		script{
		// 			branchName = env.GIT_BRANCH.split('/')[1]
		// 			dockerImage = docker.build registry +"${repoName}:${branchName}-${BUILD_NUMBER}"
		// 		}
		// 	}
		// }
		// stage('Configure Amazon AWS CLI & Image push to ECR'){
		// 	steps{
		// 		script{
		// 			docker.withRegistry('https://055638961298.dkr.ecr.us-east-1.amazonaws.com', 'ecr:us-east-1:aws_credentials') {
        //                 dockerImage.push()
        //             }
		// 		}
		// 	}
		// }
		stage('SSH to remote server and New Deployment'){
			steps{
				script{
					node{
						withDockerRegistry(credentialsId: 'dockerhub_credentials', url: '') {
							def imageName = "${registry}${repoName}:-${BUILD_NUMBER}"
							echo "$imageName"
							// sshagent(['new_sshkey']) { 
							// 	sh """
							// 	ssh -o StrictHostKeyChecking=no -l ${remoteServerName} ${remoteServerIP} \
							// 	btariq/btariq-deploy.sh $registry $repoName
							// 	"""
							// }	
						}
					}
				}
			}
		}
	}
}
