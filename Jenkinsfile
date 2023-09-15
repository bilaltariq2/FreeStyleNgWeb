pipeline{
	agent any

	environment{
		registry="btariq/jenkins-learning"
		dockerImage = ''
		fullBranchName= ''
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
					dockerImage = docker.build registry +":${branchName}-${BUILD_NUMBER}"
				}
			}
		}
		stage('Pusing Docker Image to Docker Hub'){
			steps{
				script{
					withDockerRegistry(credentialsId: 'dockerhub_credentials', url: '') {
    					dockerImage.push()
					}		
				}
			}
		}
		stage('Checkpoint for approval for New Deployment'){
			steps{
				script{
					input message: 'Are you sure to deploy a new container on Remote Server?', ok: 'Allow'
				}
			}
		}
		stage('SSH to remote server and New Deployment'){
			steps{
				script{
					node{
						withDockerRegistry(credentialsId: 'dockerhub_credentials', url: '') {
							sshagent(['new_sshkey']) { 
								sh """
								ssh -o StrictHostKeyChecking=no -l ${remoteServerName} ${remoteServerIP} \
								docker run -d --name remotenginx -p 8085:80 $registry:$branchName-${BUILD_NUMBER}
								"""
							}	
						}
					}
				}
			}
		}
		stage('Cleaning Image on Local Server'){
			steps{
				script{
					sh "docker rmi $registry:${branchName}-${BUILD_NUMBER}" 
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
