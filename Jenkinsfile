pipeline {
        agent any
        stages{
                        stage('---Build_Image---'){
                                steps{
                                        sh "sudo docker build -t flaskapp ."
                                }
                        }
                        stage('--clean--'){
                                steps{
                                       sh label: '', script: 
                                           '''
                                           if [ "$(sudo docker ps -aq -f name=flaskapp)" ]; then
                                                sudo docker rm -f flaskapp
                                           fi
                                           '''
                               }
                        }
                                              
                        stage('--run--'){
                                steps{
                                                                
                                        sh "sudo docker run -d -p 5000:5000 --name flaskapp flaskapp"
                                 
                                }
                        }
        }
}
