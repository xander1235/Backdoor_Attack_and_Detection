This program features a Linux Backdoor implementation where an attacker is able to remotely access a targeted machine and gain control of executable commands.
Files:

server.py The server is to be ran by the victim's machine. It will conceal itself and masquerade the process.

client.py The client program is to be ran by the attacker's machine. It will allow access to the victim's machine, allowing the attacker to execute any Linux commands. The privilege is based on who executed the server program.
Executables:

On the target's machine, type:

$ python server.py -p (port) &

On the attacker's machine, type:

$ python client.py -d (host ip) -p (port)

Note: Both program requires pycrypto library to be installed Additionally, the server requires the setproctitle library to be installed


