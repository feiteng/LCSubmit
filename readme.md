# Auto Submit LeetCode

## Usage:

```python
python3 autoSubmit.py s1.ini
```

where s1.ini is the config file, manually input:

- desired question 
- function signature
- default return parameter

when running this file, a testcases folder will be created to save test cases leetcode used for that particular question

## Misc

==IMPORTANT!==

- You must be logged into leetcode in order to run script, I tried to login with `csrftoken` but I cannot bypass recaptcha3 from Google. Logging in doesn't hurt anyway.
- You can manually input your `csrftoken` and `LEETCODE_SESSION` in `cookies.ini` file for the program to run correctly. 
- Or let the program read these cookies info from your `chrome browser` (for now)

Function runs with a 1 second back off time to prevent from getting rate limited from website, feel free to adjust this.

Currently this only works with single function type questions..

Inputs are hashed with a sha256 hash function, writing down all inputs will lead to lengthy code and leetcode blocks that

Theoretically it can work just like a cli, don't think it's worth to develop that functionality

There are cases with tons of testcases, leading to running for long time. e.g. 65 [valid number](https://leetcode.com/problems/valid-number/) has 1488 test cases. Although recent questions are around 50 testcases. e.g 1825. [Finding MK Average](https://leetcode.com/problems/finding-mk-average/) has 17 test cases.

This might or might not work during contest, due to hidden test cases..

## Sample video

https://youtu.be/HQL6omPfGwc

