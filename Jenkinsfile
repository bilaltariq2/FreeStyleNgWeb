pipeline{
	agent any
	stages{
		stage('Building Docker Image'){
			steps{
				script{
					def buildNumber = env.BUILD_NUMBER
					def imageName = "nginxcustomimage:${buildNumber}"
					sh "docker build -t ${imageName} ."
				}
			}
		}
	}
}
