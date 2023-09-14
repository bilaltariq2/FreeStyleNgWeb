pipeline{
	agent any

	environment{
		registry="btariq/jenkins-learning"
		dockerImage = ''
		fullBranchName= ''
		branchName = ''
	}

	stages{
		stage('Building Docker Image'){
			steps{
				script{
					fullBranchName= env.GIT_BRANCH
					branchName = fullBranchName.replaceAll('origin/', '')
					dockerImage = docker.build registry + ":${branchName}-${BUILD_NUMBER}"
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
						//withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', passwordVariable: 'dockerHubPass', usernameVariable: 'dockerHubUser')]) {
						withDockerRegistry(credentialsId: 'dockerhub_credentials', url: '') {
							sshagent(['new_sshkey']) { 
								echo "branch name is $branchName"
								sh '''
								ssh -o StrictHostKeyChecking=no -l ${remoteServerName} ${remoteServerIP} \
								docker run -d --name remotenginx -p 8082:80 $registry:echo"${branchName}"-${BUILD_NUMBER}
								'''
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
}
