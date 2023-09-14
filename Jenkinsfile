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
		stage('SSH to remote server and New Deployment'){
			steps{
				script{
					//sh "ssh ubuntu@10.24.2.170 ls"
					def remote = [:]
					remote.name = "ubuntu"
                    remote.host = "10.24.2.170"
                    remote.allowAnyHosts = true
					node{
						withCredentials([sshUserPrivateKey(credentialsId: 'new_sshkey', keyFileVariable: 'SSH_KEY_PATH', usernameVariable: 'jenkins')]) {
						remote.user = 'ubuntu'
						remote.identityFile = SSH_KEY_PATH
						stage('I am in SSH') {
							echo "SSH key file is located at: $SSH_KEY_PATH"
							sshCommand remote: remote, command: 'ls'
							}
						}
					}
				}
			}
		}
		// stage('SSH to remote server and New Deployment'){
		// 	steps{
		// 		script{
		// 			def sshCredentialsId = 'sshkey_jenkins'
		// 			sshagent(credentials: [sshCredentialsId]) {
		// 				sh '''
        //                     ssh -o StrictHostKeyChecking=no \
        //                         -o UserKnownHostsFile=/dev/null \
        //                         -i $SSH_KEY_FILE \
        //                         ubuntu@10.24.2.170 \
        //                         "ls"
        //                 '''
		// 			}su 
		// 		}
		// 	}
		// }
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

pipeline {
    agent any

    stages {
        stage('SSH to Remote Server') {
            steps {
                script {
                    // Define the credentials ID for your SSH private key
                    def sshCredentialsId = 'your_ssh_credentials_id'

                    sshagent(credentials: [sshCredentialsId]) {
                        // SSH to the remote server
                        sh '''
                            ssh -o StrictHostKeyChecking=no \
                                -o UserKnownHostsFile=/dev/null \
                                -i $SSH_KEY_FILE \
                                username@your-remote-server-ip-or-hostname \
                                "your-remote-command"
                        '''
                    }
                }
            }
        }
    }
}
