# leetcode-stats

A python script to get your own stats on leetcode.


### Motivation
I wanted to get more diversified stats of those problems I have worked on Leetcode. Due to NOT familiar with javascript/AJAX hacking, I built this python script with [Selenium](http://docs.seleniumhq.org/) and [PhantomJS](http://phantomjs.org/) to parse the problem tables.



### Prerequisite

- Selenium


```
pip install selenium
```

- PhantomJS

Download the package on [PhantomJS' website](http://phantomjs.org/). Put the `phantomjs` binary in your path.
I have tried Chrome with [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/), the PhantomJS performs better.

```bash
➜  leetcode-stats git:(master) ✗ time ./leetcode-stats.py -u xxx -p xxx
Total problems 404
--------------
Easy   problems solved: 84 / 107
Medium problems solved: 57 / 209
Hard   problems solved: 19 / 88
--------------
./leetcode-stats.py -u xxx -p xxx  2.47s user 0.44s system 9% cpu 29.814 total
➜  leetcode-stats git:(master) ✗ time ./leetcode-stats.py -u xxx -p xxx
Total problems 404
--------------
Easy   problems solved: 84 / 107
Medium problems solved: 57 / 209
Hard   problems solved: 19 / 88
--------------
./leetcode-stats.py -u xxx -p xxx  1.81s user 0.51s system 6% cpu 37.845 total
```

### Usage

```bash
➜  leetcode-stats git:(master) ✗ ./leetcode-stats.py -h
usage: leetcode-stats.py [-h] -u USERNAME -p PASSWORD [-o OUT]

extract algorithm stats from LeetCode OJ.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        website username
  -p PASSWORD, --password PASSWORD
                        website password
  -o OUT, --out OUT     dump problems in a csv file
```


