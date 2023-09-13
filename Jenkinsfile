pipeline{
	agent any

	environment{
		registry="btariq/jenkins-learning"
		dockerImage = ''
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
		stage('SSH to remote server and New Deployment'){
			steps{
				script{
					def remote = [:]
					remote.name = "ubuntu"
                    remote.host = "10.24.2.170"
                    remote.allowAnyHosts = true
					withCredentials([sshUserPrivateKey(credentialsId: 'sshkey_jenkins', keyFileVariable: 'keyfile', usernameVariable: 'ubuntu')]) {
					remote.user = ubuntu
                    remote.identityFile = keyfile
					stage('I am in shitty SSH'){
						sshCommand remote: remote, command: "mkdir /home/ubuntu/test" 
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
