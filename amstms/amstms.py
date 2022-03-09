#!/bin/python3

#
#  AMSTMS Tool it helps you to manage Projects with operations
#  such as Deploy, backup (create, load), integrity check
#  Copyright (C) 2022  Adriatik Mehmeti
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import datetime
import filecmp
import os
import pickle
from random import randint
from threading import Timer
import shutil
import time
import gc

class amstms:

    def __init__(self, cache=None):

        if os.geteuid() != 0:
            exit("You need to have root privileges.\nPlease try again.")

        if cache is None:
            self.cache = {'debug': False, 'sc': False, 'Mode': False, 'project_active': None}
        else:
            self.cache = cache
        self.services = [self.integrity]
        self.Message = {}
        self.DefaultPath = {'config': '/etc/AMSTMS/config/config.pkl',
                            'project': '/etc/AMSTMS/Projects',
                            'backupProject': '/root/AMSTMS/Backup',
                            'backupWorkdir': '/root/AMSTMS/Project',
                            'report': '/var/log/AMSTMS_error'
                            }

    def run(self):
        """###### Config LOAD ######"""
        if self.DefaultPath['config'] is not None and os.path.exists(self.DefaultPath['config']):
            with open(self.DefaultPath['config'], "rb") as data:
                config = pickle.load(data)
            self.cache['Mode'] = config['Mode']

        """###### Project LOAD ######"""
        if self.cache['project_active'] is not None and os.path.exists(
                '{}/{}'.format(self.DefaultPath['project'], self.cache['project_active'])):
            # Load Profile
            with open('{}/{}'.format(self.DefaultPath['project'], self.cache['project_active']),
                      "rb") as data:
                profile = pickle.load(data)

            # Settings Data set
            self.cache['projektNAME'] = profile['projektNAME']
            self.cache['deployPATH'] = profile['deployPATH']
            self.cache['username'] = profile['username']
            self.cache['workingPATH'] = profile['workingPATH']

        self.__init__(cache=self.cache)

    # SETTER
    def set_mode(self, status=False):

        if status:
            self.cache['Mode'] = status
            with open(f'{self.DefaultPath["config"]}', 'wb') as data:
                pickle.dump({'Mode': self.cache['Mode']}, data)
                data.close()

        return self.cache['Mode']

    def set_log(self, status=False):
        if status:
            self.cache['debug'] = status
        return self.cache['debug']

    def set_schedule(self, status=False):
        if status:
            self.cache['sc'] = status
        return self.cache['sc']

    def set_project_active(self, status=False):
        if status:
            self.scanner()
        return self.cache['project_active']
    # END SETTER

    def schedule(self, b: bool = False):

        if b:
            self.cache['sc'] = True if self.cache['sc'] is False else False

        if self.cache['sc']:

            for i in self.services:
                i()
                self.message_push(f'Success called service {randint(1, 5225)}', f'Service {i.__name__} is called by system.')
            Timer(5, self.schedule).start()

    def showlog(self, b: bool = False):

        if b:
            self.cache['debug'] = True if self.cache['debug'] is False else False

        if self.cache['debug']:
            self.clear()
            for key in self.Message:
                print(self.Message[key])
            Timer(8, self.showlog).start()

    @staticmethod
    def newdir(name):
        os.mkdir(name)

    def new_path(self, path):

        # Folder separator
        separate = '/'

        # Already discovered path
        discover = ''

        if path.count(separate) > 0:

            path = path.split(separate)[1:]

            for item in path:
                discover += '{}{}'.format(separate, item)
                status = os.path.exists(discover)
                if not status:
                    self.newdir(discover)

            return True

    def clear(self):

        os.system('clear')
        print(self.banner('intro'), '\n')

    def clear_folder(self, path):

        with os.scandir(path) as itr:
            content = list(itr)

        for item in content:
            if os.path.isfile(item):
                os.remove(item)
                self.message_push(f'path RN{randint(1, 5225)}', '{}/{}'.format(path, item.name))
            else:
                shutil.rmtree('{}/{}'.format(path, item.name), ignore_errors=False)
                self.message_push(f'path RN{randint(1, 55111)}', '{}/{}'.format(path, item.name))

    def permission_path(self, path):

        # Set Permission
        for root, dirs, files in os.walk(path):
            for d in dirs:
                os.chmod(os.path.join(root, d), 444)
            for f in files:
                os.chmod(os.path.join(root, f), 555)
        self.message_push('Permission', 'Permission Folder: 444 - File: 555')

    def load(self, last=False):
        self.clear()
        latest_copy = self.DefaultPath['backupProject']

        with os.scandir(latest_copy) as itr:
            archive = list(itr)

        if archive:

            if last:
                # Clear Deploy path
                self.clear_folder(self.cache['deployPATH'])
                self.message_push('Reset Deploy', 'Deploy path is clear.')
                # Copy from latest deploy archive
                shutil.copytree('{}/{}'.format(self.DefaultPath['backupWorkdir'], self.cache['projektNAME']),
                                self.cache['deployPATH'], dirs_exist_ok=True)

                self.message_push('Load', 'Load last backup. ')
                # Permission
                self.permission_path(self.cache['deployPATH'])

                return

            while True:

                print('\n[~] Backup Found:')
                for (i, deploy) in enumerate(archive, start=0):
                    date = deploy.name.split('@')[1]
                    print('[{}] Backup - Time : {}'.format(i, date))

                try:
                    answer = int(input('\nI want : '))
                    if answer <= len(archive):
                        shutil.copytree('{}/{}'.format(self.DefaultPath['backupProject'], archive[answer].name),
                                        self.cache['deployPATH'], dirs_exist_ok=True)
                        self.message_push('Load backup', 'Load from backup -> {}'.format(archive[answer].name))
                        del answer
                        return True

                except ValueError:
                    self.message_push('Error Value Error ', 'User typed wrong id for backup')
                    if str(input('Cancel? [Y]yes/[N]o ')).upper() == 'Y':
                        break

                del answer
                self.message_push('Error load', "Error, can't load backup")

    def message_push(self, key, msg):

        if str(key).count('Error'):
            _prefix = '[!]'
        elif str(key).count('Succe'):
            _prefix = '[+]'
        else:
            _prefix = '[#]'

        self.Message[key] = '{} {}'.format(_prefix, msg)

        del _prefix, key, msg

    def backup(self):

        last_bakFolder: str = '{}@{}'.format(str(self.cache['projektNAME']).replace(' ', '_'),
                                             str(datetime.datetime.now()).replace('_', ''))
        backup_project = '{}/{}'.format(self.DefaultPath['backupProject'], last_bakFolder)
        if backup_project:
            shutil.copytree(self.cache['deployPATH'], backup_project)

            self.message_push('Success backup', 'Successfuly backup project - Path -> {}'.format(last_bakFolder))
            time.sleep(1)
        del last_bakFolder

    def deploy(self):

        # Clear old
        self.clear_folder(self.cache['deployPATH'])

        # Copy to deploy path
        shutil.copytree(self.cache['workingPATH'], self.cache['deployPATH'], dirs_exist_ok=True)

        self.message_push('Success Deploy Project', 'Successfuly Deploy Project {}'.format(self.cache['deployPATH']))

        # Permission
        self.permission_path(self.cache['deployPATH'])

        # Clear old
        self.clear_folder('{}/{}'.format(self.DefaultPath['backupWorkdir'], self.cache['projektNAME']))

        # Copy new
        _tmp: str = '{}/{}/'.format(self.DefaultPath['backupWorkdir'], self.cache['projektNAME'])
        shutil.copytree(self.cache['workingPATH'], _tmp, dirs_exist_ok=True)

        self.message_push('Success copy deployed', 'Successfuly copy deployed project already {}'.format(_tmp))
        del _tmp

    def integrity(self):

        status = filecmp.dircmp(self.cache['deployPATH'], '{}/{}'.
                                format(self.DefaultPath['backupWorkdir'], self.cache['projektNAME']))

        if not status.diff_files and not status.left_only and not status.right_only:
            pass
        else:
            self.message_push('Error compromised', 'Deployed project is compromised! \n[*] Performing Load Backup')
            self.new_path('/var/log/AMSTMS_error/{}'.format(self.cache['projektNAME']))

            with open(f"{self.DefaultPath['report']}/{self.cache['projektNAME']}/{datetime.date.today()}", 'a+') as log:
                log.write('{} {}\n'.format('Different_Files: ', status.diff_files))
                log.write('{} {}\n'.format('Files different position: ', status.funny_files))
                log.write('{} {}\n'.format('Files in deploye which missing on backup: ', status.left_only))
                log.write('{} {}\n'.format('Files in backup which missing on deploye: ', status.right_only))
                del status
                log.close()

            self.load(last=True)

        self.message_push(f'Integrity {randint(1, 5225)}',
                          'Looks good! Time {}'.format(datetime.datetime.today().time()))

    def setup(self):

        self.clear()
        self.new_path(self.DefaultPath['backupProject'])
        self.message_push('Success Setup Backup', 'Backup Directory -> {}'.
                          format(self.DefaultPath['backupProject']))
        """###### RESET ######"""
        self.cache['projektNAME'] = None
        self.cache['username'] = None
        self.cache['deployPATH'] = None
        self.message_push('Success Setup Reset', 'Config info reset -> {}'.format('##############'))
        """###### Inputs ######"""
        while self.cache['username'] is None:
            answ: str = str(input('[?] Type username account in this system: '))
            if len(answ.strip()) > 3:
                self.cache['username'] = answ
                del answ

        while self.cache['projektNAME'] is None:
            answ: str = str(input('[?] Type Project Name: '))
            if len(answ.strip()) > 3:
                self.cache['projektNAME'] = answ
                del answ

        while self.cache['deployPATH'] is None:
            answ: str = str(input('[?] Type Path to deploy: '))
            if len(answ.strip()) > 3:
                self.cache['deployPATH'] = answ
                del answ

        """###### Entries Config ######"""
        self.new_path('{}/{}'.
                      format(self.DefaultPath['backupWorkdir'], self.cache['projektNAME']))

        self.message_push('Success Setup Backup Working Directory', 'Backup Working Directory -> {}'.
                          format(self.DefaultPath['backupWorkdir']))

        self.cache['workingPATH'] = '/home/{}/AMSTMS/Project/{}'.\
            format(self.cache['username'], self.cache['projektNAME'])

        self.new_path(self.cache['workingPATH'])

        self.message_push('Success Setup Working Directory', 'Working Directory -> {}'.
                          format(self.cache['workingPATH']))

        """###### Profile saved DATA ######"""
        # Save structured data
        profile = {'projektNAME': self.cache['projektNAME'],
                   'deployPATH': self.cache['deployPATH'],
                   'username': self.cache['username'],
                   'workingPATH': self.cache['workingPATH']
                   }

        """###### SAVE PROJECT PROFILE CONFIG ######"""
        # create file if not exist
        open('{}/{}.conf.pkl'.
             format(self.DefaultPath['project'], self.cache['projektNAME']), 'x').close()
        # write
        with open('{}/{}.conf.pkl'.format(self.DefaultPath['project'], self.cache['projektNAME']), 'wb') as output:
            pickle.dump(profile, output)
            output.close()

    def exists(self):

        if self.cache['project_active'] is None:
            self.scanner()
        if self.cache['project_active'] is not None:
            self.clear()
            if self.cache['Mode']:
                input(f"{self.banner('warDev')}\nPress Enter to continue...")
            elif not self.cache['Mode']:
                self.integrity()

            # SECOND =========
            while True:

                self.clear()
                answer = input(self.banner('Operation'))

                if int(answer.isdigit()):
                    self.tuple('second')[int(answer)]()
                elif not int(answer.isdigit()):
                    self.additional_key(answer)
                    if answer == 'back':
                        break

    def banner(self, banner):

        selected: str = str(self.cache['project_active']).split('.')[0] if self.cache[
                                                                               'project_active'] is not None else ''

        Banner = {'main': '[~] Options:\n[0] Switch Mode -> {}\n[1] New Setup\n[2] Exist Project\n\nI want : '.format(
            self.cache['Mode']),
            'Operation': '\n[~] Options:\n[0] Deploy Project\n[1] Backup Project\n[2] Load Project\n[3] Check '
                         'Integrity\n[4] Switch Project\n\nI want : ',
            'scanner': '[#] App -> Scanning\n',
            'Backup': '[#] App -> Backup\n',
            'Load': '[#] AMSTMS -> Load\n',
            'Deploy': '[#] App -> Deploy\n',
            'intro': '[#] AMSTMS v1.0. {}'.format(selected),
            'Operation phase': '[#] App -> Operations',
            'schedule': '[#] Added in schedule integrity',
            'warDev': '[*]----------------------WARNING-----------------------|\n'
                      '|                                                      |\n'
                      '| You are running under Develop Mode,                  |\n'
                      '| this prevent te check integrity of data. Develop     |\n'
                      '| Mode is recomended when you are processing data      |\n'
                      '| such as importing, exporting, modify content         |\n'
                      '| Always set Mode -> Develop when you will interact    |\n'
                      '| with data because workflow will detect difference as |\n'
                      '| such imediately will return latest backup            |\n'
                      '|                                                      |\n'
                      '[*]-----------------------END--------------------------|\n'
        }

        return Banner[str(banner)]

    def scanner(self):

        self.clear()

        with os.scandir(f'{self.DefaultPath["project"]}/') as itr:
            entries = [i.name for i in list(itr) if str(i.name).count('.conf.pkl') == 1]

        if not entries:
            input("[#] Not Found Projects\nPress Enter to continue...")
            return

        print('[~] Project found:')
        for i in range(0, len(entries)):
            print('[{}] {}'.format(i, str(entries[i]).split('.')[0]))

        try:
            answer: int = int(input('\nI want : '))
        except ValueError as e:
            return e

        self.cache['project_active'] = entries[int(answer)]
        self.message_push('Success Select project', 'Project Selected -> {}'.format(entries[int(answer)]))
        self.run()
        del answer

    def switchmode(self, mode=None):

        mode = 'Mode' if mode is None else mode

        Mode = self.tuple('switchmode')

        if mode in Mode:

            if Mode[mode]() is True:
                Mode[mode](status=False)
            else:
                Mode[mode](status=True)

    def additional_key(self, opt):
        keyword = self.tuple('keyword')
        if opt in keyword:
            keyword[opt](b=True)

    @staticmethod
    def exit(b=False):
        if b:
            if str(input('[?] Are you sure to exit ? [Y]es [N]o ')).lower().count('y'):
                exit('Program Closed.')

    def tuple(self, req):
        _tuple = {'main': [self.switchmode, self.setup, self.exists],
                 'second': [self.deploy, self.backup, self.load, self.integrity, self.scanner],
                 'keyword': {'debug': self.showlog,
                             'schedule': self.schedule,
                             'exit': self.exit},
                 'switchmode': {'Mode': self.set_mode,
                                'debug': self.set_log,
                                'sc': self.set_schedule,
                                'project_active': self.set_project_active}
                }
        if req in _tuple:
            return _tuple[req]

    def main(self):
        self.run()
        # MAIN ==========
        while True:
            self.clear()
            action = input(self.banner('main'))
            try:
                if int(action.isdigit()):
                    self.tuple('main')[int(action)]()
                elif not int(action.isdigit()):
                    self.additional_key(action)
                    time.sleep(1)
            except ValueError as h:
                self.message_push('Error Value', f'Input from user ValueError: {h}')
            except KeyboardInterrupt:
                self.clear()
                exit('Exit Program')
            except Exception as e:
                input(f'{e}\n[!] Only numbers or keyword \nPress Enter to continue...')


if __name__ == '__main__':

    AMSTMS = amstms()
    try:
        AMSTMS.main()
    except KeyboardInterrupt:
        AMSTMS.clear()
        print('Exit Program')
        del AMSTMS
        gc.collect(generation=0)
        gc.collect(generation=1)
        gc.collect(generation=2)
        print('Clear Memory')