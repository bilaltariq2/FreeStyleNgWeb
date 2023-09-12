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
		stage('SSH to remote server and deployment'){
			steps{
				script{
					def remote = [:]
					remote.name = "ubuntu"
                    remote.host = "10.24.2.193"
                    remote.allowAnyHosts = true
					node{
						withCredentials([sshUserPrivateKey(credentialsId: 'sshkey_jenkins', keyFileVariable: 'keyfile', usernameVariable: 'ubuntu')]) {
							remote.user = ubuntu
                            remote.identityFile = keyfile
						}
					}
				}
			}
		}
	}
}
