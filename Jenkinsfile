node {
    docker.withRegistry('https://newknowledge.azurecr.io', 'acr-creds') {
    
        git url: "https://github.com/newknowledge/ibex.git", credentialsId: '055e98d5-ce0c-45ef-bf0d-ddc6ed9b634a'
    
        sh "git rev-parse HEAD > .git/commit-id"
        def commit_id = readFile('.git/commit-id').trim()
        println commit_id
    
        stage "build_ibex"
        def ibex_image = docker.build("ibex")
    
        stage "publish_all"
        def images = [ibex_image]
        for (image in images) {
            image.push 'master'
            image.push "${commit_id}"
        }
    }
}
