import docker
import settings

app_settings = settings.AppSettings.get_settings()


class Hoist:
    CLIENT = docker.from_env()

    def __init__(self):
        self.Images = ["mongo:3.6", "tendermint/tendermint:v0.31.5"]
        self.dockerfile_location = app_settings['buildpath'] + "Dockerfile"
