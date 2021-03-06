# pirat-tool

[![Build Status](https://travis-ci.org/dhach/ansible-role-pirat-tool.svg?branch=master)](https://travis-ci.org/dhach/ansible-role-pirat-tool)

This role deploys all components necessary for running the [PIRAT-Tool](http://pirat-tool.com). Source Code for PIRAT-Tool is available on Github: [COVID19-PIRAT](https://github.com/COVID19-PIRAT)

Please note that this role deploys a customized software. You'll probably not be able to use it out-of-the-box and for your purposes. Instead, use this Ansible role as an easy example on how to write one yourself.

## Requirements

On the target host(s)

* SystemD
* Docker (>19.0.0)
* docker-compose (>1.17.0)

## Role Variables

All defined variables are listed below, with their respective default variables given.

### Deployment User and SystemD

Where and as whom to deploy the docker-compose file. Also controls as which user/group the service is started:

```yaml
pirat_deployment_directory: /opt/pirat/
pirat_deployment_user: root
pirat_deployment_group: docker
```

You can set the name of the systemD service:

```yaml
pirat_systemd_service_name: pirat
```

### Frontend

Which Docker image and image tag to use:

```yaml
pirat_frontend_docker_image: covid19pirat/pirat-frontend
pirat_frontend_docker_image_tag: stable
```

Map the port of the frontend's Webserver to this IP and Port:

```yaml
pirat_frontend_docker_listen_ip: 127.0.0.1
pirat_frontend_docker_listen_port: 8081
```

Optionally define additional environment variables or docker volumes to use:

```yaml
pirat_frontend_docker_environment_additional: []
pirat_frontend_docker_volumes: []
```

### Backend

**Docker**

Which Docker image and image tag to use:

```yaml
pirat_backend_docker_image: covid19pirat/pirat-backend
pirat_backend_docker_image_tag: stable
```

Whether to map the backend's port to the outside and, if so, to which IP/port:

```yaml
pirat_backend_docker_map_port: false
pirat_backend_docker_listen_ip: 127.0.0.1
pirat_backend_docker_listen_port: 5001
```

Optionally define additional environment variables or docker volumes to use:

```yaml
pirat_backend_docker_environment_additional: []
pirat_backend_docker_volumes: []
```

**Application**

If running in testing or development environments, set these to "testproduction" or "development":

```yaml
pirat_webapp_environment: production
```

If set to true, will enable access to the Swagger UI under /api/swagger/

```yaml
pirat_backend_is_development: false
```

You can change the prefix of the Swagger UI to something else:

```yaml
pirat_backend_swagger_prefix_path: /api
```

Key/Password for the admin page:

```yaml
pirat_backend_admin_key: JackSparrow
```

Database credentials.
If you choose to have the database deployed with Docker, these values will be used to set up the database.

```yaml
pirat_database_host: postgres
pirat_database_port: 5432
pirat_database_dbname: pirat
pirat_database_user: pirat
pirat_database_password: CAPTAIN_Jack_Sparrow
```

*NOTE:* If deploying the database with docker, leave `pirat_database_host` and `pirat_database_port` unchanged!

Your Google API key for geolocation services and a reCaptcha Secret for your domain

```yaml
pirat_google_api_key: nope
pirat_google_recaptcha_secret: nope
```

Configuration for sending mail

```yaml
pirat_mail_sender_address: pirat@localhost
pirat_mail_smtp_host: localhost
pirat_mail_smtp_user: pirat
pirat_mail_smtp_password: pirat
```

Send every outgoing mail as a BCC to this address:

```yaml
pirat_mail_bcc_address: pirat@localhost
```

The URL of your PIRAT Instance. Will be used in outgoing mails

```yaml
pirat_url: http://localhost
```

### Database container

Start a PostgreSQL Instance with Docker alongside the Frontend and Backend containers

```yaml
pirat_postgres_use_docker: true
```

The following variables only matter, if `pirat_postgres_use_docker` is `true`:

```yaml
pirat_postgres_docker_image: postgres
pirat_postgres_docker_image_tag: 12
pirat_postgres_persistence: true
pirat_postgres_persistence_dir: "{{ pirat_deployment_directory }}/postgres"
```

*Note*: You have to ensure that `pirat_postgres_persistence_dir` exists!

If you would like to map the database port, modify accordingly:

```yaml
pirat_postgres_map_port: false
pirat_postgres_docker_listen_ip: 127.0.0.1
pirat_postgres_docker_listen_port: 5432
```

Additional configuration parameters can be specified by defining them as a list:

```yaml
pirat_postgres_additional_config:
  - shared_buffers=256MB
  - max_connections=200
```

These parameters will be passed to the Postgresql and can be of any available option in a postgresql.conf file. (Default is an empty list)

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- hosts: pirat-server
    roles:
        - dhach.pirat_tool
    vars:
    pirat_url: https://pirat-tool.exmaple.com

    pirat_google_api_key: SuperSecretGoogleApiKey
    pirat_google_recaptcha_secret: SuperSecretGoogleReCaptchaSecret

    pirat_mail_sender_address: pirat@example.com
    pirat_mail_smtp_host: localhost
    pirat_mail_smtp_user: pirat
    pirat_mail_smtp_password: Captain_Jack_Sparrow!
    pirat_mail_bcc_address: pirat@example.com

    pirat_postgres_use_docker: true
    pirat_database_user: pirat
    pirat_database_password: CorrectHorseBatteryStable
```

(You might want to consider using Ansible Vault for any passwords or sensitive information.)

## Testing

Testing is done with Molecule and Travis. It encompasses a complete run of the playbook with default values.

## License

GPL3
