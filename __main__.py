import pulumi
import pulumi_awsx as awsx
import pulumi_eks as eks
import pulumi_kubernetes as k8s
from image import MyImage

#VPC
vpc = awsx.ec2.Vpc("eks-vpc",
    enable_dns_hostnames=True,
    cidr_block="10.0.0.0/16")

#EKS Cluster
eks_cluster = eks.Cluster("eks-cluster",
    vpc_id=vpc.vpc_id,
    public_subnet_ids=vpc.public_subnet_ids,
    private_subnet_ids=vpc.private_subnet_ids,
    instance_type="t2.medium",
    desired_capacity=1,
    min_size=1,
    max_size=1,
    node_associate_public_ip_address=False,
    endpoint_private_access=False,
    endpoint_public_access=True
    )
# Export values to use elsewhere
pulumi.export("kubeconfig", eks_cluster.kubeconfig)
pulumi.export("vpcId", vpc.vpc_id)

#TODO: args?
hello_world_image = MyImage("hello_world")

#TODO: Deploy app as k8s deployment
deployment = k8s.apps.v1.Deployment("deployment", 
    metadata=k8s.meta.v1.ObjectMetaArgs(
        labels={
            "app": "hello-world",
        },
    ),
    spec=k8s.apps.v1.DeploymentSpecArgs(
        replicas=1,
        selector=k8s.meta.v1.LabelSelectorArgs(
            match_labels={
                "app": "hello-world",
            },
        ),
        template=k8s.core.v1.PodTemplateSpecArgs(
            metadata=k8s.meta.v1.ObjectMetaArgs(
                labels={
                    "app": "hello-world",
                },
            ),
            spec=k8s.core.v1.PodSpecArgs(
                containers=[k8s.core.v1.ContainerArgs(
                    image=hello_world_image.hello_world.image_name,
                    name="hello-world",
                    ports=[k8s.core.v1.ContainerPortArgs(
                        container_port=8080,
                    )],
                )],
            ),
        ),
    ))