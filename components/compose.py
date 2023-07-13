from python_on_whales import DockerClient


class Compose:
    def __init__(self):
        # From config file:
        # client_call=["nerdctl"]
        # client_call=["podman"]
        # client_call=["docker"]
        self.docker = DockerClient(client_call=["docker"],
                                   compose_files=["./composes/orionld.yml"],
                                   compose_env_file="./composes/.env")

    def up(self):
        self.docker.compose.build()
        self.docker.compose.up(detach="True")

    def down(self):
        self.docker.compose.down(volumes="True")
