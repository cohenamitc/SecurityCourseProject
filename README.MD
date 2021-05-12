# Communication LTD

### Docker image build
```bash
$ docker build . -t communication_ltd:latest
```

### Docker Run
```bash
$ docker run -p 5000:5000 -p 2222:2222 --name "communication_ltd_web" communication_ltd:latest
```

### Docker stop
```bash
$ docker stop communication_ltd_web
```

### Docker remove
```bash
$ docker rm communication_ltd_web
```

### Push to ACR
```bash
$ az acr build --registry <acr-name> --image communication_ltd .
```