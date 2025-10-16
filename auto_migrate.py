#!/usr/bin/env python3
"""
Auto-migration wrapper using pexpect to handle interactive prompts
Usage: python3 auto_migrate.py [SOURCE_TYPE] [DG_NAME] [DEST_TYPE] [DEST_NAME] [FETCH] [CERT] [ARGS...]
"""

import sys
import pexpect

def run_migration(source_type, dg_name, dest_type, dest_name, fetch, cert, args):
    """Run migration with automatic prompt responses"""
    
    print("Configuration:")
    print(f"  Source Type: {source_type}")
    print(f"  Device Group: {dg_name}")
    print(f"  Destination Type: {dest_type}")
    print(f"  Destination Name: {dest_name}")
    print(f"  Fetch Config: {fetch}")
    print(f"  Accept Cert: {cert}")
    print()
    
    # Build the command
    cmd = f"python3 main.py {' '.join(args)}"
    
    # Spawn the process
    child = pexpect.spawn(cmd, encoding='utf-8', timeout=300)
    child.logfile = sys.stdout
    
    try:
        # Q1: Do you want to retrieve new config?
        child.expect('Do you want to retrieve new config', timeout=30)
        child.sendline(fetch)
        print(f">> Sent: {fetch}")
        
        # Q2: Untrusted certificate? (only if fetching AND cert prompt appears)
        if fetch.lower() == 'yes':
            # Wait for either cert prompt OR the next question
            idx = child.expect(['Untrusted certificate', "'shared'"], timeout=30)
            if idx == 0:  # Certificate prompt appeared
                child.sendline(cert)
                print(f">> Sent: {cert}")
                # Now wait for shared/device-group question
                child.expect("'shared'", timeout=30)
            # If idx == 1, we already matched the shared question, continue
        
        # Q3: shared or device-group? (already matched if cert wasn't asked)
        child.sendline(source_type)
        print(f">> Sent: {source_type}")
        
        # Q4: Device group name (only if device-group)
        if source_type == 'device-group':
            child.expect('device-group name', timeout=30)
            child.sendline(dg_name)
            print(f">> Sent: {dg_name}")
        
        # Q5: folder or snippet?
        child.expect(['folder', 'snippet'], timeout=30)
        child.sendline(dest_type)
        print(f">> Sent: {dest_type}")
        
        # Q6: folder/snippet name
        child.expect('name', timeout=30)
        child.sendline(dest_name)
        print(f">> Sent: {dest_name}")
        
        # Wait for completion
        child.expect(pexpect.EOF, timeout=600)
        child.close()
        
        return child.exitstatus if child.exitstatus is not None else 0
        
    except pexpect.TIMEOUT as e:
        print(f"\n\n❌ Error: Timeout waiting for prompt")
        print(f"Expected pattern didn't appear")
        print(f"Last output before timeout:")
        print(child.before)
        print(f"\nBuffer:")
        print(child.buffer)
        child.close()
        return 1
    except pexpect.EOF:
        print("\n\n✓ Process completed")
        child.close()
        return child.exitstatus if child.exitstatus is not None else 0
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        child.close()
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: auto_migrate.py SOURCE_TYPE DG_NAME DEST_TYPE DEST_NAME FETCH CERT [MAIN.PY ARGS]")
        print("\nExample:")
        print("  python3 auto_migrate.py device-group aa-home folder aa-home yes yes -o Tag")
        sys.exit(1)
    
    source_type = sys.argv[1]
    dg_name = sys.argv[2]
    dest_type = sys.argv[3]
    dest_name = sys.argv[4]
    fetch = sys.argv[5]
    cert = sys.argv[6]
    main_args = sys.argv[7:]
    
    exit_code = run_migration(source_type, dg_name, dest_type, dest_name, fetch, cert, main_args)
    sys.exit(exit_code)
