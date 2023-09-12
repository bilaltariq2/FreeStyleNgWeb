pipeline{
	agent any

	environment{
		registry="btariq/jenkins-learning"	
	}

	stages{
		stage('Building Docker Image'){
			steps{
				script{
					def buildNumber = env.BUILD_NUMBER
					def branchName = env.GIT_BRANCH
					dockerImage = docker.build registry + ":${branchName}-${buildNumber}"
				}
			}
		}
		stage('Pusing Docker Image to Docker Hub'){
			steps{
				withDockerRegistry(credentialsId: 'dockerhub_credentials') {
    				dockerImage.push()
				}		
			}
		}
	}
}
