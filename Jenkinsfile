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
            		bash -c "docker run --rm -e SONAR_HOST_URL=http://192.168.1.102:9000  -v $(pwd):/usr/src sonarsource/sonar-scanner-cli sonar-scanner -Dsonar.projectKey=django -Dsonar.login=1fc9c40a655b18f70a4e9c413b0d5a377b8bbdbb"
                '''
            }
        }  
  }
}
