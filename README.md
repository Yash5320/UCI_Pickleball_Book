## Features

- Logs in with your **UCInetID and password**
- Handles **Duo 2FA**, you'll need to approve duo in your phone
- Checks all facilities for booking slots 2 days ahead
- Automatically books the **first 2 available slot**
---


## Setup Instructions
Create `.env` and update with your credentials:

```env
UCI_ID=your_ucinetid
UCI_PASSWORD=your_password
```

### Setting Up cron
For mac: use crontab to run court_book.py every night @ 12:00 AM
https://www.youtube.com/watch?v=QZJ1drMQz1A&t=4s

some useful commands

update:
```
crontab -l > ~/Desktop/my_crontab.txt
```
make changes
```
crontab ~/Desktop/my_crontab.txt
```

View crons
```
crontab -l
```
