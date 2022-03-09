<h3>AMSTMS - STORAGE TASK MANAGMENT SYSTEM</h3>

<hr/>
<ul>
<li>Author: Adriatik Mehmeti</li>
<li>Tool: AMSTMS</li>
<li>Version: 1.0</li>
<li>Year: 2022</li>
<li>Type: Open Source</li>
</ul>
<hr/>

<h4> Information </h4>
<p>Tool operate under <b>Options</b> and <b>Keyword</b></p>
<p>Options: Switch Mode, New Setup, Exist Project</p>

<small>[ - ] ------------------------------------ Options ------------------------------------ [ - ]</small>
<h5>Switch Mode</h5>
<p>This option control mods, when is enable check integrity on 
select project.<br/>
It has two state: True, False</p>

<h5>New Setup</h5>
<p>This option create configuration for new project like Setup Wizard
and you just need follow the instructions presented by output console.<br/>
Required:</p>

<ul><li>User Account</li>
<li>Project Name</li>
<li>Deploy Path (When you need to deploy in remote server try port forwarding
<b>[SSH]</b> or samba )</li>
</ul>

<h5>Exist Project</h5>
<p>This option scan for existing projects to load configuration to 
be able to operate</p>

<p>Operation <b>Deploy</b> phase:<br/> 
1) Firstly cleans Deploy folder<br/>
2) Copies Project from Working Directory to Deploy Path<br/>
3) Applies predefined privileges on Deploy<br/>
4) Cleans the last backup of working directory<br/>
5) Make a backup of working directory to user <b>root/Administrator</b>
</p>

<p>Operation <b>Backup</b> performs copy of the Project in Deploy to backup path
in directory to user <b>root/Administrator</b></p>

<p>Operation <b>Load</b> has two options:</p>
<ul>
<li>Last - ( It means automaticaly load backup of working directory )</li>
<li>Manual ( Select backup to load )</li>
</ul>

<p>In each of case get backups from path which are predefined under DEFAULT_PATH
and replace with </p>

<p>Operation <b>Check Integrity</b> performs of a comparison of Deployed Project 
with the latest condition</p>

<p>Operation <b>Switch Project</b> performs scan for project registered</p>

<small>[ - ] ------------------------------------ Keyword ------------------------------------ [ - ]</small>

<p>Keyword List</p>
<ul>
<li>Debug - Command: debug</li>
<li>Schedule - Command: schedule</li>
<li>Exit - Command: exit</li>
</ul>

<p><b>Debug</b> activates output logs generated from tasks</p>
<p><b>Schedule</b> activates auto execute tasks which are defined on constructor </p>
<p><b>Exit</b> Close activities and cleans memory</p>

<small>[ - ] ------------------------------------ Usage ------------------------------------ [ - ]</small>

<p> You most select an Project to be abile to start schedule via keyword</p>
<p> Keywords can typed instead of number which can identify task</p>

<small>[ - ] ------------------------------------ FEATURES PRO  ------------------------------------ [ - ]</small>

<p>Remote backup: [SSH] [SFTP] [FTP]</p>
<p>Hash content table: [md5] [Sha1] [sha256]</p>
<p>Lock down</p>
