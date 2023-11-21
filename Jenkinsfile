node {
    def app

    // Stage 1: Clone repository
    stage('Clone repository') {
        checkout scm
    }

    // Stage 2: Build image
    stage('Build image') {
        app = docker.build("kevinwynn/test")
    }

    // Stage 3: Test image
    stage('Test image') {
        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    // Stage 4: Push image to DockerHub
    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            app.push("${env.BUILD_NUMBER}")
        }
    }

    // Stage 5: Trigger ManifestUpdate job
    stage('Trigger ManifestUpdate') {
        echo "Triggering updatemanifestjob"
        build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
    }
}
