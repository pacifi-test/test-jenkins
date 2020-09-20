// comment
pipeline {
 agent any
 stages {
        stage('Checkout-git'){
               steps{
		git poll: true, url: 'https://github.com/pacifi-test/test-jenkins.git'
               }
        }
       
    
          stage('TestApp') {
            steps {
            	sh '''
            		bash -c "docker run --rm --net host -e SONAR_HOST_URL=http://192.168.1.102:9000  -v $(pwd):/usr/src sonarsource/sonar-scanner-cli sonar-scanner -Dsonar.projectKey=django -Dsonar.login=7b5c95e163fc23627e2ef4da9e46d645fdd57c10"
                '''
            }
        }  
  }
}
