pipeline{
	agnet any

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
		stage('Removing previous running container'){
			steps{
				script{
					sh"docker rm -f freestylenginx"
				}
			}
		}
		stage('Deploying new container'){
			steps{
				script{
					sh "docker run -d --name freestylenginx -p 8082:80 freenginx:${buildNumber}"
				}
			}
		}
	}
}
