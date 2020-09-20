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
            		bash -c "docker run --rm sonarsource/sonar-scanner-cli  -Dsonar.projectKey=django -Dsonar.host.url=http://192.168.1.102:9000  -Dsonar.login=7c76b6f2ed3a5f41293ceca2697ae6b08141a640"
                '''
            }
        }  
  }
}
