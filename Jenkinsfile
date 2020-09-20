// comment
pipeline {
 agent any
 stages {
        stage('Checkout-git'){
               steps{
		git poll: true, url: 'https://github.com/pacifi-test/test-jenkins.git'
               }
        }
        stage('SonarTests') {
        docker.image('newtmitch/sonar-scanner').inside('-v /var/run/docker.sock:/var/run/docker.sock') {
            sh "/usr/local/bin/sonar-scanner -Dsonar.host.url=http://192.168.1.102:9000 -Dsonar.sources=. -Dsonar.projectKey=django -Dsonar.login=c7119df2065124e06e2b7289263d863fa984d1be"
        }
    }
          stage('TestApp') {
            steps {
            	sh '''
            		bash -c "docker run --rm -e SONAR_HOST_URL="http://192.168.1.102:9000" -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli -Dsonar.projectKey=django -Dsonar.login=c7119df2065124e06e2b7289263d863fa984d1be"
                '''
            }
        }  
  }
}
