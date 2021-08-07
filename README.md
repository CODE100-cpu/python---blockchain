### Prerequisites

- **Python 3.8** 
- `pip` version 9.0.1 or higher
- macOS (V11.1)
If necessary, upgrade your version of `pip`:
```sh
$ python3 -m pip install --upgrade pip
```
Then we need to install all dependencies within our virtual environment 
```sh
$ cd VaccineSystem
$ source venv/bin/activate 
$ pip install -r requirements.txt
```
### Python MongoDB using Atlas & pymongo
We do not want to deploy our system locally since it is difficult to collaborate. Thus we choose [Atlas](https://www.mongodb.com/cloud/atlas), a cloud-based mongoDB service. Follow this [tutorial](https://www.youtube.com/watch?v=rE_bJl2GAY8) to establish your Atlas platform. My **connection string** is as follows. Note that we set **ssl_cert_reqs=ssl.CERT_NONE** for simplicity despitet that it is not a good option concerning network security. 
```sh
client = MongoClient("mongodb+srv://minghui:minghui@cluster0.86rir.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
```
Then we install the pymongo library
```sh
$ python3 -m pip install pymongo # skip this if you have installed dependencies following requirements.txt
$ mongo --verions #macOS
```
Our databased is named as "blockchian", and the collection is "blocks" which sequentially stores all blocks 
Tutorials:
Blog: https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
Video: https://www.youtube.com/watch?v=rE_bJl2GAY8

### Run!
Open a terminal and run:
```sh
$ python3 blockchain_server.py

The Genesis block is created!
Blockchain Database is established!
generate a new block
{'index': 1, 'timestamp': 1628319479.6583989, 'transactions': [], 'proof': 100, 'previous_hash': '1'}
genesis block= {'index': 1, 'timestamp': 1628319479.6583989, 'transactions': [], 'proof': 100, 'previous_hash': '1'}
 * Serving Flask app 'blockchain_server' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://192.168.1.104:5000/ (Press CTRL+C to quit)
```
Then see the welcome page on http://<IP>:5000/
Besides, you can also  test the blockchain server with Postman or Curl commands. 

```sh
[GET] http://192.168.1.104:5000/mine
# Output
generate a new block
{'index': 2, 'timestamp': 1628319515.638013, 'transactions': [{'sender': '0', 'recipient': '752e8aac6ffd44bb89032d75043c8080', 'amount': 1, 'latitude': 0, 'altitude': 0, 'x_axis_acceler': 0, 'y_axis_acceler': 0, 'z_axis_acceler': 0, 'humidity': 0, 'temperature': 0, 'lx': 0}], 'proof': 25647, 'previous_hash': '1e7422a945a499c7fbbed818a127dd1dfe0f4d83e4d34686c3f59b033f6d709f'}
192.168.1.104 - - [07/Aug/2021 14:58:35] "GET /mine HTTP/1.1" 200 -
```

### Clean PORT
Clean ports being used if something bad happens
```sh
$ ./test.sh
```
### Homebrew
Update homebrew using Tsinghua mirrors
```sh
$ cd /usr/local/Homebrew
$ git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git
$ cd /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core
$ git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git
$ brew update
```



