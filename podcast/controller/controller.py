import kubernetes as kube
from config import kubeconfig


casts = {}


def create_job(app_id, image="podcastsh/cast-sh:dev", namespace="default"):

    kube.config.load_kube_config(kubeconfig)

    obj_meta = kube.client.V1ObjectMeta(
        labels={
            "app": "cast-{}".format(app_id)
        },
        name="cast-{}".format(app_id))

    isgx = kube.client.V1VolumeMount(
        mount_path="/dev/isgx",
        name="dev-isgx"
    )

    devisgx = kube.client.V1Volume(
        name="dev-isgx",
        host_path=kube.client.V1HostPathVolumeSource(
            path="/dev/isgx"
        )
    )

    container_spec = kube.client.V1Container(
        image=image,
        image_pull_policy="Always",
        name="cast-{}".format(app_id),
        tty=True,
        volume_mounts=[isgx],
        security_context=kube.client.V1SecurityContext(
            privileged=True
        ))

    pod_spec = kube.client.V1PodSpec(
        containers=[container_spec],
        restart_policy="OnFailure",
        volumes=[devisgx])

    pod = kube.client.V1PodTemplateSpec(
        metadata=obj_meta,
        spec=pod_spec)

    job_spec = kube.client.V1JobSpec(
        parallelism=1,
        template=pod)

    job = kube.client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=obj_meta,
        spec=job_spec)

    batch_v1 = kube.client.BatchV1Api()
    job = batch_v1.create_namespaced_job(namespace, job)

    port = create_service(app_id)

    ip = get_node_ip()

    return {"url": "{}:{}".format(ip, port)}


def create_service(app_id, namespace="default"):

    svc_meta = {
        "name": "cast-{}".format(app_id),
        "labels": {
            "app": "cast-{}".format(app_id)
        }
    }

    svc_spec = {
        "ports": [{
            "protocol": "TCP",
            "port": 5000,
            "targetPort": 5000
        }],
        "selector": {
            "app": "cast-{}".format(app_id)
        },
        "type": "NodePort"
    }

    CoreV1Api = kube.client.CoreV1Api()

    svc = kube.client.V1Service(
        spec=svc_spec, api_version="v1", kind="Service", metadata=svc_meta)

    s = CoreV1Api.create_namespaced_service(
        namespace=namespace, body=svc)
    node_port = s.spec.ports[0].node_port

    return node_port


def get_node_ip():
    nodes = kube.client.CoreV1Api().list_node().items
    for node in nodes:
        is_ready = [s for s in node.status.conditions if s.type ==
                    'Ready'][0].status == 'True'
        if is_ready:
            node_info = node

    addresses = node_info.status.addresses

    url = addresses[0].address
    for address in addresses:
        if (address.type) == "ExternalIP":
            url = address.address
    return url