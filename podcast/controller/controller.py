import kubernetes as kube
from config import kubeconfig


def create_job(app_id, cmd, img):

    kube.config.load_kube_config(kubeconfig)

    obj_meta = kube.client.V1ObjectMeta(
        name=app_id)

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
        command=cmd,
        image=img,
        image_pull_policy="Always",
        name=app_id,
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
    batch_v1.create_namespaced_job("default", job)

    return job
