
from __future__ import print_function
import sys, os
import getpass
import subprocess
from distutils.dir_util import copy_tree
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
	
	print('Raspberry Smart Cam Installer')
	print('-----------------------------\n')
	
	if not is_raspberry():
		print('Script can only be run on a Raspberry Pi')
		
	elif not is_root():
		print('Script can only be run as root')
		
	else:
		
		user = getpass.getuser()
		
		install_dir = prompt('Please specify where to install the project : ')
		while not install_dir.strip():
			install_dir = prompt('Please specify a valid path : ');
		while not os.path.isabs(install_dir):
			install_dir = prompt('Only absolute paths are allowed : ');		
		while os.path.exists(install_dir) and len(os.listdir(install_dir)) != 0:
			install_dir = prompt('Directory is not empty please specify another path : ');
		
		print('')
		
		launcher_file = os.path.join(install_dir, 'launcher.sh')
		
		settings_file = os.path.join(install_dir, 'settings.py')

		print('+ Installing motion...')
		exec_command('sudo apt-get update')
		exec_command('sudo apt-get -y install motion')
		print('')
		
		print('+ Updating /etc/motion/motion.conf...')
		local_motion_conf = 'conf/motion.conf'
		with open(local_motion_conf, 'r') as file:
			data = file.read()
			data = data.replace('PYTHON_BIN', sys.executable)
			data = data.replace('INSTALL_DIR', install_dir)
			motion_conf = '/etc/motion/motion.conf'
			with open(motion_conf, 'w+') as file:
				file.seek(0)
				file.write(data)
				file.truncate()
		print('')
		
		print('+ Copying files to ' + install_dir + '...')
		copy_tree('app', install_dir)
		with open(launcher_file, "r+") as file:
			data = file.read()
			data = data.replace('INSTALL_DIR', install_dir)
			data = data.replace('PYTHON_BIN', sys.executable)
			file.seek(0)
			file.write(data)
			file.truncate()
		print('')
		
		print('+ Changing permissions of ' + install_dir + '...')
		cmd = 'sudo chown ' + user + ':' + user + ' -R ' + install_dir
		exec_command(cmd)
		cmd = 'sudo chmod +x ' + launcher_file
		exec_command(cmd)
		print('')
		
		print('+ Updating crontab...')
		cron = CronTab(user=user)
		job = cron.new(command=launcher_file)
		job.every_reboot()
		cron.write()
		print('')
				
		print('> Successfully installed the program at ' + install_dir)
		print('> Change sim card pin and phone number in ' + settings_file)
		print('> Make sure that the camera and the serial port are enabled otherwise the program will not work')

		
