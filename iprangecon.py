import sys
import pandas as pd
import ipaddress

def parse_ip_range(ip_range_str):
    if '-' in ip_range_str:
        start_ip, end_ip = ip_range_str.split('-')
        ip_range = list(ipaddress.IPv4Network(f"{start_ip}-{end_ip}", strict=False))
        return ip_range
    else:
        return [ip_range_str]

def file_to_ip_list(input_file):
    df = pd.read_csv(input_file)
    ip_list = df['IP Range'].apply(parse_ip_range).explode().tolist()
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
