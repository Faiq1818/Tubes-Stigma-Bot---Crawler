#!/bin/bash

python main.py --logic Random --email=test11@email.com --name=random --password=123456 --team etimo &
python main.py --logic Crawler --email=test12@email.com --name=crawler --password=123456 --team etimo &
python main.py --logic Crawler --email=test121@email.com --name=crawler22 --password=123456 --team etimo &
python main.py --logic Crawler --email=test123@email.com --name=crawler33 --password=123456 --team etimo &
# python main.py --logic Hasil --email=test2@email.com --name=stima2 --password=123456 --team etimo &
# python main.py --logic Random --email=test3@email.com --name=stima3 --password=123456 --team etimo &
