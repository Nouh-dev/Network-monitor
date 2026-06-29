import nmap

def detecter_os(target):
    scanner = nmap.PortScanner(
        nmap_search_path=(
            r"C:\Program Files (x86)\Nmap\nmap.exe",
        )
    )

    scanner.scan(target, arguments="-O -T4 --host-timeout 10s ")

    for host in scanner.all_hosts():

        os_matches = scanner[host].get("osmatch", [])

        if len(os_matches) > 0:

            best_os = os_matches[0]

            return best_os["name"]

    return " "