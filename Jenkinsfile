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
						//def branchName = env.GIT_BRANCH.split('/')[1]
						//imageTag = "${branchName}-141" 
                    }
                }
            }
        }
		stage('Building Docker Image'){
			steps{
				script{
					def branchName = env.GIT_BRANCH.split('/')[1]
					imageTag = "${branchName}-${BUILD_NUMBER}"
					dockerImage = docker.build registry +"${repoName}:${imageTag}"
				}
			}
		}
		stage('Configure Amazon AWS CLI & Image push to ECR'){
			steps{
				script{
					docker.withRegistry('https://055638961298.dkr.ecr.us-east-1.amazonaws.com', 'ecr:us-east-1:aws_credentials') {
                        dockerImage.push()
                    }
				}
			}
		}
		// stage{
		// 	steps{
		// 		script{
		// 			echo "Image tag is ${imageTag}"
		// 		}
		// 	}
		// }
		// stage('SSH to remote server and New Deployment'){
		// 	steps{
		// 		script{
		// 			node{
		// 				def imageName = "${registry}${repoName}:${imageTag}"
		// 				sshagent(['new_sshkey']) { 
		// 					sh """
		// 					ssh -o StrictHostKeyChecking=no -l ${remoteServerName} ${remoteServerIP} \
		// 					btariq/btariq-deploy.sh AWS $registry $imageName
		// 					"""
		// 				}	
		// 			}
		// 		}
		// 	}
		// }
		// stage('Cleaning Image on Local Server'){
		// 	steps{
		// 		script{
		// 			sh "docker rmi ${registry}${repoName}:${imageTag}" 
		// 		}
		// 	}
		// }
	}
	// post{
	// 	success{
	// 		emailext attachLog: true, body: 'Build has been completed.', subject: 'Build Success', to: 'b4bylal@gmail.com'
	// 	}
	// 	failure{
	// 		emailext attachLog: true, body: 'Build has been failed.', subject: 'Build Failed', to: 'b4bylal@gmail.com'
	// 	}
	// }
}
