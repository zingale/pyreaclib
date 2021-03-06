# Test the examples against the outputs in their corresponding ./standard/... subdirectories
from __future__ import print_function
import os
import shutil
import datetime
import subprocess
import nose.tools

# Setup some directory names
dir_test = os.path.dirname(os.path.realpath(__file__))
dir_reaclib = os.path.split(dir_test)[0]
dir_examples = os.path.join(dir_reaclib, 'examples')
dir_runs = os.path.join(dir_test, 'runs')
dir_standard = os.path.join(dir_test, 'standard')

# Make a list of test cases from the directories in pyreaclib/test/standard
test_cases = []
for entry in os.listdir(dir_standard):
    if os.path.isdir(os.path.join(dir_standard, entry)):
        test_cases.append(entry)

# Use the current date and time to create a unique testrun directory name
dtnow = datetime.datetime.now()
sdtnow = dtnow.strftime("%Y-%m-%d--%H-%M-%S-%f")
dir_now = os.path.join(dir_runs, sdtnow)
# Make a directory for these tests in runs
os.mkdir(dir_now)
print('Using test suite directory {}'.format(dir_now))

def test_all():
    for tc in test_cases:
        print('\nTesting {}:\n'.format(tc))
        
        # Make dirs and copy script file
        dir_tc = os.path.join(dir_now, tc)
        dir_std_tc = os.path.join(dir_standard, tc)
        os.mkdir(dir_tc)
        example_path = os.path.join(dir_examples, tc)
        script_name = tc.split('_')[0].lower() + '.py'
        for file in os.listdir(example_path):
            shutil.copy(os.path.join(example_path, file), dir_tc)
        os.chdir(dir_tc)

        # Run test case
        pycall = subprocess.Popen(['python',script_name],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        pycall_stdout, pycall_stderr = pycall.communicate()

        if pycall_stderr:
            print('Error in python call of script {}:'.format(os.path.join(dir_tc, script_name)))
            print(pycall_stderr)
            exit()

        # Compare with standard
        for file in os.listdir(dir_std_tc):
            f_tc = os.path.join(dir_tc, file)
            f_std_tc = os.path.join(dir_std_tc, file)
            diffcall = subprocess.Popen(['diff', f_tc, f_std_tc],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            diffcall_stdout, diffcall_stderr = diffcall.communicate()

            if diffcall_stderr:
                print('Error in diff call between {} and {}:'.format(f_tc, f_std_tc))
                print(diffcall_stderr)
                exit()

            yield nose.tools.assert_equals, diffcall_stdout, ''
    

