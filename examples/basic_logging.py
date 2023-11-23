# Copyright (c) 2023 Purvish Jajal
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from picoboard import PicoLogger

if __name__ == "__main__":
    # This creates a log file in the example_logs directory. 
    # The logfile is named as follows "%Y-%m-%dT%H:%M:%S-{log_comment}.log" 
    # In this case if will be "%Y-%m-%dT%H:%M:%S-basic_logging.log"
    plog = PicoLogger(log_dir="./example_logs", log_comment="basic_logging")

    # This logs a set of scalars to the file.
    some_test_numbers = [0.55, 0.23, 1.23, 9.42, 0.44]
    for num in some_test_numbers:
        # names are NOT case sensitive!!
        # all spaces are replaced with hypens
        plog.log_scalar("validation accuracy", f"{num:0.2f}")
    