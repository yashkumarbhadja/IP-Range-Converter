import sys
import pandas as pd
import ipaddress

def parse_ip_range(ip_range_str):
    ips = ip_range_str.split('-')

    if len(ips) == 2:
        start_ip, end_ip = ips

        start_ip_obj = ipaddress.IPv4Address(start_ip)
        end_ip_obj = ipaddress.IPv4Address(end_ip)

        ip_list = [str(ipaddress.IPv4Address(ip)) for ip in range(int(start_ip_obj), int(end_ip_obj) + 1)]

        return ip_list
    else:
        try:
            # Attempt to convert to IPv4Address
            ipaddress.IPv4Address(ip_range_str)
            return [ip_range_str]
        except ipaddress.AddressValueError:
            # If not a valid IPv4Address, return the original string
            return [ip_range_str]

def file_to_ip_list(input_file):
    df = pd.read_csv(input_file, dtype=str)
    ip_list = df.iloc[:, 0].apply(parse_ip_range).explode().tolist()
    return ip_list

def ip_list_to_csv(ip_list, output_file):
    df = pd.DataFrame(ip_list, columns=['IP'])
    df.to_csv(output_file, index=False)
    print(f"IP list converted to CSV: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file.csv output_file.csv")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    output_csv_file = sys.argv[2]

    ip_list = file_to_ip_list(input_csv_file)

    # Manipulate the IP list if needed

    ip_list_to_csv(ip_list, output_csv_file)
