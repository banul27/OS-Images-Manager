import docker
from docker.errors import NotFound


def start_container(image_name):
    client = docker.from_env()
    return client.containers.run(image_name, detach=True)


def stop_container(container_id):
    client = docker.from_env()
    try:
        client.containers.get(container_id).stop()
    except NotFound:
        pass  # already removed from Docker (prune, restart, manual delete)


def restart_container(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.start()
    return container
