import unittest
import parse_file
from collections import defaultdict

class TestFileParser(unittest.TestCase):

    def test_case_insensitive(self):

        input_log_flow = ['2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 22 6 25 20000 1620140761 1620140821 ACCEPT OK', 
                          '2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 2312 23 6 15 12000 1620140761 1620140821 REJECT OK', 
                          '2 123456789012 eni-5e6f7g8h 192.168.1.101 198.51.100.3 25 49155 6 10 8000 1620140761 1620140821 ACCEPT OK', 
                          '2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 110 49156 6 12 9000 1620140761 1620140821 ACCEPT OK']
        
        input_lookup_list = [['dstport,protocol,tag'],
                            ['25,tcp,sv_P1'], 
                             ['68,udp,sv_P2'], 
                             ['23,tcp,email'], 
                             ['31,udp,SV_P3'], 
                             ['22,tcp,Email']]
        
        actual_tag_count , actual_port_protocol_count = parse_file.files_parser(input_log_flow, input_lookup_list)

        expected_tag_count = {
            'email': 2, 'Untagged': 2
        }

        excepted_port_protocol_count = {
            ('22', 'tcp'): 1, ('23', 'tcp'): 1, ('49155', 'tcp'): 1, ('49156', 'tcp'): 1
        }
        
        self.assertEqual(actual_tag_count, expected_tag_count)
        self.assertEqual(actual_port_protocol_count, excepted_port_protocol_count)

    def test_multiple_valid_protocol(self):

        input_log_flow = ['2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 23 6 25 20000 1620140761 1620140821 ACCEPT OK', 
                          '2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 2312 68 17 15 12000 1620140761 1620140821 REJECT OK', 
                          '2 123456789012 eni-5e6f7g8h 192.168.1.101 198.51.100.3 25 49155 6 10 8000 1620140761 1620140821 ACCEPT OK', 
                          '2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 110 49156 6 12 9000 1620140761 1620140821 ACCEPT OK',
                          '2 123456789012 eni-9h8g7f6e 172.16.0.100 203.0.113.102 110 31 17 12 9000 1620140761 1620140821 ACCEPT OK',
                          '2 123456789012 eni-9h8g7f6f 172.16.0.100 203.0.113.102 110 49156 6 12 9000 1620140761 1620140821 ACCEPT OK',]
        
        input_lookup_list = [['dstport,protocol,tag'],
                            ['25,tcp,sv_P1'], 
                             ['68,udp,email'], 
                             ['23,tcp,email'], 
                             ['31,udp,SV_P3'], 
                             ['22,tcp,sms']]
        
        actual_tag_count , actual_port_protocol_count = parse_file.files_parser(input_log_flow, input_lookup_list)

        expected_tag_count = {
            'email': 2, 'Untagged': 3, 'sv_p3': 1
        }

        excepted_port_protocol_count = {
            ('23', 'tcp'): 1, ('68', 'udp'): 1, ('49155', 'tcp'): 1, ('49156', 'tcp'): 2, ('31', 'udp'): 1
        }
        
        self.assertEqual(actual_tag_count, expected_tag_count)
        self.assertEqual(actual_port_protocol_count, excepted_port_protocol_count)

if __name__ == '__main__':
    unittest.main()