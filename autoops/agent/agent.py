import time
from autoops.core.core import get_system_state, is_service_running, fix_service, analyze_and_act

#make simple code
def main():
    while True:
        analyze_and_act()
        time.sleep(30) #each 30 sec working

if __name__ == "__main__":
    main()
