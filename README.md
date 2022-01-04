# sent
Your climbing data for the year, sent!


## running the backend
The backend is setup to run locally for devlopment using docker-compose. The command: `docker-compose up` should be all
you need to get it started. After running that command, the service should be available on localhost port 8080.

### submitting an example file
The following HTTPie command can be used to post an example file:
```bash
http -f POST :8080/send file@path/to/csv/file.csv
```
