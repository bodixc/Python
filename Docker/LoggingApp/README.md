Python Interactive LogsApp
    You can change the delay in config/config.yaml -> parameter: delayInSec

Requires: Installed Docker

Config -> Dockerfile

Build command:
    docker build -t pylogs .
        - pylogs - image name in lowercase!

Run container (interactive mode):
    docker run -e user=$(whoami) -v py_logs:/app/logs -v $pwd/config:/app/config --name logsapp pylogs
        -e user=$(whoami)           -   creates ENV variable user -> value = user who runs this container
        -v py_logs:/app/logs        -   creates named volume py_logs -> /app/logs
        -v $pwd/config:/app/config  -   creates mount bind ./config -> /app/config
        --name logsapp              -   set container's name logsapp in lowercase!
        - pylogs                    -   image name

Show Logs:
    docker exec py cat /app/logs/write.log