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
            		bash -c "docker run --rm -v $(pwd):/usr/src newtmitch/sonar-scanner sonar-scanner -Dsonar.projectKey=django -Dsonar.login=ab44807c428f4385064b545c2aef9be186f55a56 -Dsonar.projectBaseDir=/usr/src -Dsonar.host.url=http://192.168.1.102:9000" 
                '''
            }
        }  
  }
}
