# Name: Mohammad Khosravi
## Student ID: 99105407
### Code Description:
The code comprises of two parts:
1. handling http (plain text)
2. handling https (encrypted)

In the first part, we simply send the request to the destination and wait till all of the
response is available. Note that we need to shut down channels that we are not going to use.

In the second part, we use two threads that communicate to the destination and client.

We have used thread pool of size 4 in order to achieve concurrency.
Not that I have commented logging lines in order to have a cleaner experience running the code!