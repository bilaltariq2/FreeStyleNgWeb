pipeline{
	agent any

	environment{
		registry="btariq/jenkins-learning"
		dockerImage = ''
		SSH_KEY_PATH = ''
	}

	stages{
		stage('Building Docker Image'){
			steps{
				script{
					def buildNumber = env.BUILD_NUMBER
					def fullBranchName= env.GIT_BRANCH
					def branchName = fullBranchName.replaceAll('origin/', '')
					dockerImage = docker.build registry + ":${branchName}-${buildNumber}"
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
		// stage('SSH to remote server and New Deployment'){
		// 	steps{
		// 		script{
		// 			def remote = [:]
		// 			remote.name = "ubuntu"
		// 			remote.host = "10.24.2.170"
		// 			remote.allowAnyHosts = true
		// 			node{
		// 				 withCredentials([sshUserPrivateKey(credentialsId: 'new_sshkey', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
		// 					remote.user = userName
		// 					remote.identityFile = identity
		// 					stage("SSH Steps Rocks!") {
		// 						sshCommand remote: remote, command: 'ls'
		// 					}
		// 				}
		// 			}
		// 		}
		// 	}
		// }
		stage('SSH to remote server and New Deployment'){
			steps{
				script{
					node{
						//withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', passwordVariable: 'dockerHubPass', usernameVariable: 'dockerHubUser')]) {
						withDockerRegistry(credentialsId: 'dockerhub_credentials', url: '') {
							sshagent(['new_sshkey']) {
							def buildNumber = env.BUILD_NUMBER
							def fullBranchName= env.GIT_BRANCH
							def branchName = fullBranchName.replaceAll('origin/', '')
							sh '''
							ssh -o StrictHostKeyChecking=no -l ${remoteServerName} ${remoteServerIP} \
							ls; \
							docker run -d --name remotenginx -p 8082:80 $registry:${branchName}-${BUILD_NUMBER}
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
					def fullBranchName= env.GIT_BRANCH
					def branchName = fullBranchName.replaceAll('origin/', '')
					//sh "docker rmi $registry:${branchName}-${buildNumber}" 
				}
			}
		}
	}
}
