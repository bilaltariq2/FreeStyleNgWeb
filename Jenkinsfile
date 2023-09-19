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
					def remote = [:]
                    remote.name = "ubuntu"
                    remote.host = "10.24.2.170"
                    remote.allowAnyHosts = true
                    node {
                        withCredentials([sshUserPrivateKey(credentialsId: 'new_sshkey', keyFileVariable: 'keyfile', usernameVariable: 'ubuntu')]) {
                            remote.user = ubuntu
                            remote.identityFile = keyfile
                            stage("SSH Steps Rocks!") {
                                // AWS Credentials
								sshCommand remote: remote, command:"ls"
                                withCredentials([[
                                    $class: 'AmazonWebServicesCredentialsBinding',
                                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY',
                                    credentialsId: 'aws_credentials'
                                ]]) {
                                    def imageName = "${registry}rashid/test:hassan-${BUILD_NUMBER}"
									sshCommand remote: remote, command: "aws ecr list-images --repository-name rashid/test"
                                    //sshCommand remote: remote, command: "./deploy-hassan.sh AWS $imageName $registry"
                                    //sshCommand remote: remote, command: "aws sts get-caller-identity"
                                }
                            }
                        }
                    }
				}
			}
		}
	}
}
