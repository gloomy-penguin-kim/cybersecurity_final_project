import pexpect 

 
child = pexpect.spawn("msfconsole")  
line_number = 1
 

child.expect(pexpect.TIMEOUT, timeout=20)
#child.expect("Metasploit Documentation.*") 
child.expect("msf6.*") 

def spawn_msf_child():  
    try: 
        child = pexpect.spawn("msfconsole")  
        line_number = 1

        print(str(child))

        child.expect(pexpect.TIMEOUT, timeout=20)
        #child.expect("Metasploit Documentation.*") 
        child.expect("msf6.*") 

    except Exception as err:
        spawn_msf_child()
 