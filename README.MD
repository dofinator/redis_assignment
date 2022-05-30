# Usage

### Start by activating the virtual enviroment with following command, standing in the root of the project:
```bash
source venv/Scripts/activate
```

### Run the docker-compose.yml file to start docker container, standing in the docker-redis folder:
```bash
docker-compose up
```

### Run the following command activating the flask server
```bash
python run.py
```

### Assignment requirements:
1. Use Redis to enhance secondary respond times from these end points.
2. Make use Redis to drill down in to the data and find some interesting point that can be fetched and displayed without the need to re-query the API all the time.
3. Divide the data in to logical divisions using either sets, lists,hashed or one of the other types native to Redis.
4. Specify a retention time for all values (Time to live)

### Info
Each assignment requirement is commented in the source file run.py, each related to an anpoint fulfilling the requirements
