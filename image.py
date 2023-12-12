import pulumi
import pulumi_docker as docker
#from pulumi_awsx import ecr

#TODO: Add arguments
# Containerized app component resource
class MyImage(pulumi.ComponentResource):
    def __init__(self, name, opts = None):
        super().__init__('pkg:index:MyImage', name, None, opts)

#TODO: create ECR repo resource
#repository = ecr.Repository()

# Build image
#TODO: make image update dynamic, switch from docker hub to ecr
    hello_world = docker.Image("hello_world",
        build=docker.DockerBuildArgs(
            args={
                "platform": "linux/amd64",
            },
            context=".",
            dockerfile="Dockerfile",
        ),
        image_name="docker.io/tryan225/hello_world:v0.1.0",
        skip_push=True)
    pulumi.export("imageName", hello_world.image_name)
    pulumi.export("repoDigest", hello_world.repo_digest)

#TODO: publish to ECR?
