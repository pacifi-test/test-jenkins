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
            		bash -c "docker run --rm -e SONAR_HOST_URL="http://192.168.1.102:9000" -v "$(pwd):/usr/src" sonarsource/sonar-scanner-cli -Dsonar.projectKey=django -Dsonar.login=c48da5608591a076f796d757fbf837d2f2120bb1" 
                '''
            }
        }  
  }
}
