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
	}
	post{
		success{
			emailext attachLog: true, body: 'Build has been completed.', subject: 'Build Success', to: 'btariq@stellatechnology.com'
		}
		failure{
			emailext attachLog: true, body: 'Build has been failed.', subject: 'Build Failed', to: 'btariq@stellatechnology.com'
		}
	}
}
