pipeline{
	agent any

	stages{
		stage('Build docker image'){
			steps{
				script{
					def buildNumber = env.BUILD_NUMBER
					def imageName = "freenginx:${buildNumber}"
					sh "docker build -t ${imageName} ."
				}
			}
		}
	}
}
