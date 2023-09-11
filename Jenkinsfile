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
		stage('Checkpoint for approval'){
			steps{
				script{
					input message: 'Do you want remove previously deployed container & deploy a new container?', ok: 'Allow'
				}
			}
		}
		stage('Removing previous running container'){
			steps{
				script{
					sh "docker rm -f freestylenginx"
				}
			}
		}
		stage('Deploying new container'){
			steps{
				script{
					def buildNumber = env.BUILD_NUMBER
					sh "docker run -d --name freestylenginx -p 8082:80 freenginx:${buildNumber}"
				}
			}
		}
		stage{
			steps{
				script{
					emailext body: 'New deployment has been made.', subject: 'New deployment for Project "Learning pipeline Jenkins"', to: 'b4bylal@gmail.com'
				}
			}
		}
	}
}
