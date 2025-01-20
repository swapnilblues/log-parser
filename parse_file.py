import csv
from collections import defaultdict
with open('input_lookup_table.csv', 'r') as input_lookup_file, open('input_log_flow.txt','r') as input_log_flow:

    input_log_flow = input_log_flow.read()
    input_log_flow = input_log_flow.split('\n')
    input_lookup_list = list(csv.reader(input_lookup_file, delimiter="\t"))
    
    def files_parser(input_lookup_list, input_log_flow):
    
        port_protocol_map = {}

        protocol_map = {
            '6' : 'tcp',
            '17' : 'udp'
        }

        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)

        for i in range(1, len(input_lookup_list)):
            dstport, protocol, tag = input_lookup_list[i][0].split(',')
            port_protocol_map[(dstport,protocol.lower())] = tag

        for line in input_log_flow:
            data = line.split()
            dstport = data[6]
            protocol = data[7]

            if protocol in protocol_map:
                protocol = protocol_map.get(protocol)
                port_protocol_counts[(dstport,protocol.lower())] += 1

            if (dstport,protocol.lower()) in port_protocol_map:
                tag = port_protocol_map[(dstport,protocol.lower())]
                tag_counts[tag] += 1
            else:
                tag_counts['Untagged'] += 1

        return tag_counts, port_protocol_counts
    
    def output_file_writer(tag_counts,port_protocol_counts):

        output_file = open('output.txt', 'w')

        # write tag counts
        output_file.write('Tag Counts:\n')
        output_file.write('Tag, Count\n')
        
        for key,val in tag_counts.items():
            output_file.write(key + ', ' + str(val) + '\n')

        # write port-protocol counts
        output_file.write('Port/Protocol Combination Counts:\n')
        output_file.write('Port, Protocol, Count\n')
        
        for key,val in port_protocol_counts.items():
            output_file.write(key[0] + ', ' + key[1] + ', ' + str(val) + '\n')

        output_file.close()

tag_counts, port_protocol_counts = files_parser(input_lookup_list, input_log_flow)
output_file_writer(tag_counts, port_protocol_counts)