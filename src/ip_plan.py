import ipaddress
import csv
import os
from datetime import datetime
from tabulate import tabulate

def generate_ip_plan(network_input, new_prefix):
    # Opret network-objekt
    network = ipaddress.ip_network(network_input, strict=False)
    subnets = list(network.subnets(new_prefix=new_prefix))

    plan = []
    for subnet in subnets:
        hosts = list(subnet.hosts())
        if not hosts:
            continue

        plan.append({
            "Subnet": str(subnet),
            "Network": str(subnet.network_address),
            "Subnet Mask": str(subnet.netmask),
            "Wildcard Mask": str(ipaddress.IPv4Address(int(subnet.hostmask))),
            "Gateway": str(hosts[0]) if hosts else "-",
            "First Host": str(hosts[1]) if len(hosts) > 1 else "-",
            "Last Host": str(hosts[-1]) if hosts else "-",
            "Broadcast": str(subnet.broadcast_address),
            "Hosts": len(hosts)
        })

    return plan

def save_to_csv(plan):
    os.makedirs("output", exist_ok=True)
    filename = f"output/ip_plan_{datetime.now().strftime('%Y-%m-%d')}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=plan[0].keys())
        writer.writeheader()
        writer.writerows(plan)
    print(f"[✔] CSV gemt som {filename}")

def save_to_markdown(plan):
    filename = f"output/ip_plan_{datetime.now().strftime('%Y-%m-%d')}.md"
    table = tabulate(plan, headers="keys", tablefmt="github")
    with open(filename, "w") as f:
        f.write("# Automatisk IP-plan\n\n")
        f.write(f"Genereret: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(table)
    print(f"[✔] Markdown gemt som {filename}")

def main():
    print("=== IP Plan Generator ===")
    network_input = input("Indtast netværk (fx 10.10.0.0/16): ")

    try:
        new_prefix = int(input("Ønsket subnet (fx 24): "))
    except ValueError:
        print("[X] Ugyldigt input – subnet skal være et tal, fx 24.")
        return

    try:
        network = ipaddress.ip_network(network_input)
    except ValueError:
        print("[X] Ugyldigt netværk. Husk at inkludere CIDR, fx 192.168.0.0/24.")
        return
    
    if new_prefix <= network.prefixlen:
        print(f"[X] Ugyldigt: {new_prefix} skal være større end {network.prefixlen} for at dele netværket op.")
        return

    plan = generate_ip_plan(network_input, new_prefix)
    print("\nEksempel:")
    print(tabulate(plan[:5], headers="keys", tablefmt="fancy_grid"))
    
    save_to_csv(plan)
    save_to_markdown(plan)

if __name__ == "__main__":
    main()
