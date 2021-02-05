
from __future__ import print_function
import sys, os
import getpass
import subprocess
import shutil
from crontab import CronTab

def prompt(helper=''):
	if sys.version_info.major == 2:
		return raw_input(helper)
	else:
		return input(helper)
	

def is_raspberry():
	try:
		return os.uname()[1] == 'raspberrypi'
	except:
		return False
	
	
def is_root():
	return os.geteuid() == 0


def exec_command(cmd):
	try:
		subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
	except:
		pass
		

if __name__ == '__main__':
	
	print('')
	
	print('Raspberry Smart Cam Uninstaller')
	print('-----------------------------\n')
	
	if not is_raspberry():
		print('Script can only be run on a Raspberry Pi')
		
	elif not is_root():
		print('Script can only be run as root')
		
	else:
		
		user = getpass.getuser()
		
		install_dir = prompt('Please specify where the project was installed : ')
		while not install_dir.strip():
			install_dir = prompt('Please specify a valid path : ');
		while not os.path.isabs(install_dir):
			install_dir = prompt('Only absolute paths are allowed : ');		
		while not os.path.exists(install_dir):
			install_dir = prompt('Directory does not exist please specify another path : ');
		
		print('')
		
		launcher_file = os.path.join(install_dir, 'launcher.sh')
				
		launcher_log = os.path.join(install_dir, 'launcher.log')

		print('+ Removing program path...')
		shutil.rmtree(install_dir)
		print('')
		
		print('+ Removing motion...')
		exec_command('sudo apt-get remove --purge motion')
		exec_command('sudo apt-get autoremove --purge')
		print('')
		
		print('+ Removing job from crontab...')
		cron = CronTab(user=user)
		command = launcher_file + ' >> ' + launcher_log + ' 2>&1'
		for job in cron:
			if job.command == command:
				cron.remove(job)
				cron.write()		
		print('')
				
		print('> Successfully removed  ' + install_dir)
		print('> Successfully uninstalled motion')
		print('> Successfully removed crontab job')

		
