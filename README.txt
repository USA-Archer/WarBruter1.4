###############################################
# __      __        ___          _     Ver1.4 #
# \ \    / /_ _ _ _| _ )_ _ _  _| |_ ___ _ _  #
#  \ \/\/ / _` | '_| _ \ '_| || |  _/ -_) '_| #
#   \_/\_/\__,_|_| |___/_|  \_,_|\__\___|_|   #
#                               by USA~Archer #
###############################################

http://USA-Archer.com/

# WarBruter Ver1.4 by USA-Archer
# Email: archer@usa-archer.com
# This program bruteforces PvPGN accounts using a password list

    Copyright (C) 2015 USA-Archer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.

DISCLAIMER: Please do not use in military or secret service organizations or
for illegal purposes.


DESCRIPTION:
- WarBruter bruteforces PvPGN accounts using a password list
- Support for username, and server lists allow for unattended
- bruteforcing of multiple accounts on multiple servers consecutively

INSTRUCTIONS:
- [Required] Install Python 2.7
- [Required] Unzip WarBruter to your PC
- [Required] All folders must be present for WarBruter to run
- Configure your settings in configuration_files directory
- Double click to run WarBruter1.4, or from cmd line "python warbruter1.4.py"

Known Issues:
- If an account is currently logged in, and the correct password is attempted, 
- the account will NOT be cracked and the password will not appear in 
- cracked_list.txt. This occurs because the server reports "Login Failed" due
- to the account already being logged in. 
- There is no work around for this other than to only use WarBruter against 
- accounts that are not currently logged in.

RELEASE NOTES:
Ver 1.4
- Directory structure
- Error checking for filenames
- Error checking for server timeout/IP Ban with option to continue (after 
- changing your IP address/VPN recommended).
- Positive identification of 'cracked' logins. Previously the logic was "if 
- not 'failed' then cracked" but this caused problems when no data was received 
- back and an account was then incorrectly marked as cracked. No more false 
- positives will occur due to lack of response from server.
- Related to the previous resolved issue, there is now an "error_log.txt" which 
- contains combinations that were not positively identified as either 'failed' 
- or 'cracked' and are stored to be either retried or reviewed later.
- Bug Fix. Calculation of per minute/per second tries was previously incorrect:
- after an account was cracked, the remaining attempts were being calculated as
- having been attempted already which boosted the per min/per sec values up. 
- Now this has been fixed, attempts that are not tried due to crack are not 
- calculated into speed equations.

Ver 1.3
- Added consecutive multi server support: server_list.txt
- Speed improvements
- ASCII art key for password found screens
- 'Finish screen' summary page enhanced
- Progress indicators for time elapsed, estimated time remaining,
- number of passwords remaining for current username, number of total tries
- remaining, average tries per minute, average tries per second

Ver 1.2
- Multi username support: user_list.txt as input for username list. 
- Unattended bruteforce of all names in list. For example WarBruter will try 
- 'user1, pass1, user1, pass2, user2, pass1, user2, pass2' etc... If any 
- account is cracked, the output will be saved to cracked_list.txt and 
- WarBruter will continue on to the next username.
- Misc user experience enhancements: 'Accounts cracked = #' summary at end of 
- cracking, progress indicators: 'Now trying <username> ...', 'Attempts 
- Remaining for this username = #'

Ver 1.1
- Added server name to cracked_list.txt output

Ver 1.0
- Initial working version, single username, single server mode only