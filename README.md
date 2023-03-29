# Sentry leak

This repository is part of the report on memory leak that caused by sentry-sdk.

## Description

You could see in the results below, that in version `1.15.0` memory footprint
stays the same, whereas in version above `1.15.0`  in continues to increase.


## Tested
Machine info:
```
Python 3.8.10 (default, Mar 13 2023, 10:26:41) 
[GCC 9.4.0]

NAME="Ubuntu"
VERSION="20.04.6 LTS (Focal Fossa)"

5.15.0-67-generic
```

Versions affected:
```
sentry-sdk==1.16.0-1.18.0
```

Latest not affected version: `1.15.0`

## Steps to reproduce

Not affected version:
```
# console 1
make compose-up
# console 2
virtualenv .venv
source ./.venv/bin/activate

export SENTRY_DSN=<your sentry dsn>

make install-deps-no-leak 
make worker-run
# console 3
source ./.venv/bin/activate

export SENTRY_DSN=<your sentry dsn>

make send-messages

```
Results in:
```
[2023-03-29 17:53:21,978: INFO/MainProcess] Task person[51f14047-6166-4cdb-8530-4afc3421d439] received
[2023-03-29 17:53:21,979: WARNING/ForkPoolWorker-1] Memory ar the beginning of the task: 42.84375 Mb
[2023-03-29 17:53:21,990: INFO/MainProcess] Task person[42f223b8-d4a6-4faf-9002-4686728099be] received
[2023-03-29 17:53:22,004: INFO/MainProcess] Task person[d946962f-2257-4cd2-93c4-9875aabef98e] received
[2023-03-29 17:53:22,019: INFO/MainProcess] Task person[e2fdf587-481c-4719-a2d9-52e82e6214cb] received
[2023-03-29 17:53:23,585: INFO/ForkPoolWorker-1] Task person[51f14047-6166-4cdb-8530-4afc3421d439] succeeded in 1.6059546929973294s: None
[2023-03-29 17:53:23,588: WARNING/ForkPoolWorker-1] Memory ar the beginning of the task: 1875.03125 Mb
[2023-03-29 17:53:25,097: INFO/ForkPoolWorker-1] Task person[42f223b8-d4a6-4faf-9002-4686728099be] succeeded in 1.5093810299986217s: None
[2023-03-29 17:53:25,098: WARNING/ForkPoolWorker-1] Memory ar the beginning of the task: 1880.81640625 Mb
[2023-03-29 17:53:26,601: INFO/ForkPoolWorker-1] Task person[d946962f-2257-4cd2-93c4-9875aabef98e] succeeded in 1.5030249129995354s: None
[2023-03-29 17:53:26,603: WARNING/ForkPoolWorker-1] Memory ar the beginning of the task: 1880.9765625 Mb
[2023-03-29 17:53:28,082: INFO/ForkPoolWorker-1] Task person[e2fdf587-481c-4719-a2d9-52e82e6214cb] succeeded in 1.4797731800026668s: None
```

Affected version:
```
# console 1
make compose-up
# console 2
virtualenv .venv
source ./.venv/bin/activate

export SENTRY_DSN=<your sentry dsn>

make install-deps-leak 
make worker-run
# console 3
source ./.venv/bin/activate

export SENTRY_DSN=<your sentry dsn>

make send-messages
```

Results in:
```
[2023-03-29 18:03:10,550: WARNING/ForkPoolWorker-1] Memory ar the beginning of the task: 43.01953125 Mb
[2023-03-29 18:03:10,561: INFO/MainProcess] Task person[a47ccff2-62ff-4980-91b7-c7e829f4b6c9] received
[2023-03-29 18:03:10,572: INFO/MainProcess] Task person[c2e4a967-cff0-4c9f-b355-99fd96eb61f4] received
[2023-03-29 18:03:10,583: INFO/MainProcess] Task person[255ebe02-0917-45f0-9f95-24906ce33444] received
[2023-03-29 18:03:12,090: INFO/ForkPoolWorker-1] Task person[4fa0b073-365e-4825-9fc9-c27e81fbee14] succeeded in 1.540306661001523s: None
[2023-03-29 18:03:12,091: WARNING/ForkPoolWorker-1] Memory ar the beginning of the task: 1876.953125 Mb
[2023-03-29 18:03:13,576: INFO/ForkPoolWorker-1] Task person[a47ccff2-62ff-4980-91b7-c7e829f4b6c9] succeeded in 1.48509692999869s: None
[2023-03-29 18:03:13,577: WARNING/ForkPoolWorker-1] Memory ar the beginning of the task: 3708.18359375 Mb
[2023-03-29 18:03:15,061: INFO/ForkPoolWorker-1] Task person[c2e4a967-cff0-4c9f-b355-99fd96eb61f4] succeeded in 1.4840153909972287s: None
[2023-03-29 18:03:15,062: WARNING/ForkPoolWorker-1] Memory ar the beginning of the task: 3852.87890625 Mb
[2023-03-29 18:03:16,694: INFO/ForkPoolWorker-1] Task person[255ebe02-0917-45f0-9f95-24906ce33444] succeeded in 1.6321742350010027s: None
```