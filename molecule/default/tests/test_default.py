import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pirat_compose_file(host):
    pirat_docker_compose = host.file('/opt/pirat/docker-compose.yml')
    assert pirat_docker_compose.exists
    assert pirat_docker_compose.user == 'root'
    assert pirat_docker_compose.group == 'docker'
    assert "FIND_ME" in pirat_docker_compose.content_string


def test_pirat_images_present(host):
    images = [ 'covid19pirat/pirat-backend', ' covid19pirat/pirat-frontend' ]
    for img in images:
        image_present = host.run("docker image history {0}:stable".format(img))
        assert image_present.rc == 0


def test_pirat_service_running(host):
    gitea = host.service('pirat')
    assert gitea.is_running


def test_pirat_reachable(host):
    endpoints = [ 'http://localhost:8081', 'http://localhost:5000' ]
    for e in endpoints:
        http_curl = host.run('curl {0}'.format(e))
        assert http_curl.rc == 0
