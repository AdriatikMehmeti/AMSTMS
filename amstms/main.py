from amstms import amstms
import gc
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
