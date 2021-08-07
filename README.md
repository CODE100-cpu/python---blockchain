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
A simple runs:
```sh
open a terminal and run
$ python3 blockchain_server.py
```
Then see the welcome page on http://192.168.1.105:5000/
Besides, you can also  test the blockchain server with Postman or Curl commands. 
### Clean PORT
Clean ports being used if something bad happen
```sh
./test.sh
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



