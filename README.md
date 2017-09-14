install deps:
    $ sudo pip2 install -r requirements.txt

run like:

    $ python2 run.py --serial-test-device=/dev/ttyACM0 --serial-dut=/dev/ttyACM1 -v

Tests to run or not to run can be configured using markers. Following markers are currently used:
- band433
- lora

When adding `-m "<marker>"` only the tests which are marked with <marker> will run.
This can also be negated by using `not <marker>` and markers can be combined using `and`/`or`.
