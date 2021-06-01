# Communication LTD installation guide
***
## *Running on Docker* 
This guide is written for Git Bash Windows users or any other Linux-like env
## 1. Database installation
Please use MS SQL Express 2019 from here
https://go.microsoft.com/fwlink/?linkid=866658

Connection string will be in the following format
```
mssql+pyodbc://<macine-name>\<cluster-name>/<db-name>?driver=SQL Server Native Client 11.0?trusted_connection=yes?UID=<db-user>?PWD=<password>
```
 Parameter | Default | Comment 
 --- | --- | --- 
macine-name | PC Name | Enter your PC name here
cluster-name | MSSQL cluster name| defined on SQL Express installation
db-name | cybercourse | Make sure DB is already present in SQL Express (tables are created automatically)
username | sa | 
password | undefinded | 

## 2. Generating private and public keys
* *REQUIRED - openssl in PATH and available to run from anywhere*

    *To test this run from project root directory*
        ```
        openssl version
        ```

    *Desired output looks like*
        ```
        OpenSSL 1.1.1i  8 Dec 2020
        ```

From project root folder run the following commands:
```bash
cd certs
./generate_cert.sh
```

## 3. Environment Variables
Copy attached "local_env.list" file to root directory of the project (same as Dockerfile directory)
```bash
cp path/to/local_env.list project/root/directory/local_env.list
```

Desired state on root project will be:
```bash
ls
app/  app.db  certs/  config/  config.py  Dockerfile  init.sh*  local_env.list README.MD requirements.txt  run.py  sshd_config  utils/ 
```
Make sure you see Dockerfile and local_env.list together

## 4. Build Docker Image
### Docker image build
```bash
docker build . -t communication_ltd:latest
```

### Docker Run
```bash
docker run -p 5000:5000 --name "communication_ltd_web" --env-file ./local_env.list communication_ltd:latest
```

## 4. Browse to app
https://127.0.0.1:5000


## 5. Close the app
#### Docker remove ()
```bash
docker rm communication_ltd_web
```