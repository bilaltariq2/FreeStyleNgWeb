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
					def branchName = env.GIT_LOCAL_BRANCH
					echo branchName
					//dockerImage = docker.build registry + ":${branchName}-${buildNumber}"
				}
			}
		}
		// stage('Pusing Docker Image to Docker Hub'){
		// 	steps{
		// 		script{
		// 			withDockerRegistry(credentialsId: 'dockerhub_credentials', url: '') {
    	// 			dockerImage.push()
		// 		}
		// 		}		
		// 	}
		// }
	}
}
