# Communication LTD

### Docker image build
```buildoutcfg
$ docker build . -t communication_ltd:latest
```

### Docker Run
```buildoutcfg
$ docker run -p 5000:5000 -p 2222:2222 --name "communication_ltd_web" communication_ltd:latest
```

### Docker stop
```buildoutcfg
$ docker stop communication_ltd_web
```

### Docker remove
```buildoutcfg
$ docker rm communication_ltd_web
```