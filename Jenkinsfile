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
		stage('Fetching Image Digest & Generating PDF Report'){
			steps{
				script{
					scanStatus = sh(script: "aws ecr describe-images --repository-name ${repoName} --image-ids imageTag=${imageTag} --query 'imageDetails[0].imageScanStatus.status' --output text", returnStdout: true).trim()
					while(scanStatus == 'IN_PROGRESS'){
						echo"AWS ECR Image Scan is in Process. Waiting to complete..."
						sleep(3)
						scanStatus = sh(script: "aws ecr describe-images --repository-name ${repoName} --image-ids imageTag=${imageTag} --query 'imageDetails[0].imageScanStatus.status' --output text", returnStdout: true).trim()	
					}
					imageDigest = sh(script: "aws ecr describe-images --repository-name ${repoName} --image-ids imageTag=${imageTag} --query 'imageDetails[0].imageDigest' --output text", returnStdout: true).trim()
					sh "aws ecr describe-image-scan-findings --repository-name ${repoName} --image-id imageDigest=${imageDigest} >> scanData.txt"
					sh "python3 main.py"
					sh "bash email.sh"
				}
			}
		}
		stage('SSH to remote server and New Deployment'){
			steps{
				script{
					node{
						def imageName = "${registry}${repoName}:${imageTag}"
						sshagent(['new_sshkey']) { 
							sh """
							ssh -o StrictHostKeyChecking=no -l ${remoteServerName} ${remoteServerIP} \
							btariq/btariq-deploy.sh AWS $registry $imageName
							"""
						}	
					}
				}
			}
		}
		stage('Cleaning Image on Local Server'){
			steps{
				script{
					sh "docker rmi ${registry}${repoName}:${imageTag}" 
					sh "rm scanData.txt"
				}
			}
		}
	}
	post{
		success{
			emailext attachLog: true, body: 'Build has been completed.', subject: 'Build Success', to: 'b4bylal@gmail.com'
		}
		failure{
			emailext attachLog: true, body: 'Build has been failed.', subject: 'Build Failed', to: 'b4bylal@gmail.com'
		}
	}
}
