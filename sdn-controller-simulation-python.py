#SDN Controller Simulation


import random
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

#Simulates a basic SDN Controller that manages network devices and flow rules
class SDNController:
    
    def __init__(self, name, controller_type="OpenFlow"):
        self.name = name
        self.controller_type = controller_type
        self.switches = {}  # Stores switch objects
        self.topology = defaultdict(list)  # Network topology
        self.flow_tables = defaultdict(list)  # Flow rules for each switch
        self.active = False
        self.performance_metrics = {
            'packet_processing_time': [],
            'flow_table_hits': 0,
            'flow_table_misses': 0,
            'controller_requests': 0
        }
        print(f"SDN Controller '{name}' ({controller_type}) initialized")
    
# Function to start the controller
    def start(self):
        self.active = True
        print(f"Controller '{self.name}' is now active")
# Function to sto the controller
    def stop(self):
        self.active = False
        print(f"Controller '{self.name}' has been stopped")
# Function to add a new switch with the controller
    def add_switch(self, switch_id, num_ports):

        if not self.active:
            print("Cannot add switch: Controller is not active")
            return False
            
        self.switches[switch_id] = {
            'id': switch_id,
            'ports': num_ports,
            'status': 'active',
            'connected_hosts': [],
            'packet_count': 0
        }
        print(f"Switch {switch_id} with {num_ports} ports added to the network")
        return True
# Function to add a new connection between two points in the existing network
    def add_connection(self, source, target):

        if source not in self.topology:
            self.topology[source] = []
        if target not in self.topology[source]:
            self.topology[source].append(target)
            print(f"Connection added from {source} to {target}")
# Function to add a flow rule to a switch
    def add_flow_rule(self, switch_id, match_criteria, action):

        if switch_id not in self.switches:
            print(f"Error: Switch {switch_id} does not exist")
            return False
# The higher the number, the higher the priority
        rule = {
            'priority': len(self.flow_tables[switch_id]) + 1, 
            'match': match_criteria,
            'action': action,
            'counter': 0,
            'created_at': time.time()
        }
        
        self.flow_tables[switch_id].append(rule)
        #print(f"Flow rule added to switch {switch_id}: {match_criteria} -> {action}")
        return True
    
# Function to simulate packet processing through SDN switch
    def process_packet(self, switch_id, packet):
        if switch_id not in self.switches:
            print(f"Error: Switch {switch_id} does not exist")
            return
        
        start_time = time.time()
        self.switches[switch_id]['packet_count'] += 1
        
        #print(f"Processing packet on switch {switch_id}: {packet}")
        
        # Look for matching flow rule
        matched_rule = None
        for rule in self.flow_tables[switch_id]:
            matches = True
            for key, value in rule['match'].items():
                if key not in packet or packet[key] != value:
                    matches = False
                    break
                    
            if matches:
                matched_rule = rule
                matched_rule['counter'] += 1
                self.performance_metrics['flow_table_hits'] += 1
                break
        
        # Apply action if rule found, otherwise send to controller
        if matched_rule:
            result = self.execute_action(switch_id, packet, matched_rule['action'])
        else:
            self.performance_metrics['flow_table_misses'] += 1
            self.performance_metrics['controller_requests'] += 1
            result = self.handle_unknown_flow(switch_id, packet)
        
        # Record processing time
        end_time = time.time()
        processing_time = (end_time - start_time) * 1000  # Convert to ms
        self.performance_metrics['packet_processing_time'].append(processing_time)
        
        return result

# Function to handle packets that have no matching flow rule
    def handle_unknown_flow(self, switch_id, packet):
        # Allow HTTP traffic (port 80)
        if packet.get('dst_port') == 80:
            match = {'src_ip': packet['src_ip'], 'dst_port': 80}
            action = {'forward_port': 2}
            self.add_flow_rule(switch_id, match, action)
            return self.execute_action(switch_id, packet, action)
        # Allow HTTPS traffic (port 443)
        elif packet.get('dst_port') == 443:
            match = {'src_ip': packet['src_ip'], 'dst_port': 443}
            action = {'forward_port': 2}
            self.add_flow_rule(switch_id, match, action)
            return self.execute_action(switch_id, packet, action)
        # Allow DNS traffic (port 53)
        elif packet.get('dst_port') == 53:
            match = {'src_ip': packet['src_ip'], 'dst_port': 53}
            action = {'forward_port': 3}
            self.add_flow_rule(switch_id, match, action)
            return self.execute_action(switch_id, packet, action)
        # Drop all other traffic
        else:
            return {'status': 'dropped'}
        
        # Drop all other traffic
        


# Function to execute the action which is specified by a flow rule
    def execute_action(self, switch_id, packet, action):
        if 'forward_port' in action:
            port = action['forward_port']
            return {'status': 'forwarded', 'port': port}
        elif 'drop' in action:
            return {'status': 'dropped'}
        elif 'modify' in action:
            fields = action['modify']
            for field, value in fields.items():
                packet[field] = value
            return {'status': 'modified', 'packet': packet}
    
# Function to display the network topology
    def show_topology(self):
        print("\nNetwork Topology:")
        print("----------------")
        for source, targets in self.topology.items():
            print(f"{source} connected to: {', '.join(targets)}")

# Function to show all flow tables currently in the network
    def show_flow_tables(self):
        print("\nFlow Tables:")
        print("-----------")
        for switch_id, rules in self.flow_tables.items():
            print(f"Switch {switch_id}:")
            for rule in rules:
                print(f"  Priority {rule['priority']}: {rule['match']} -> {rule['action']} (hits: {rule['counter']})")
            print("")
# Function to print a performance report for the controller
    def get_performance_report(self):

        if not self.performance_metrics['packet_processing_time']:
            return "No performance data available yet"
            
        avg_processing_time = sum(self.performance_metrics['packet_processing_time']) / len(self.performance_metrics['packet_processing_time'])
        
        hit_ratio = 0
        if (self.performance_metrics['flow_table_hits'] + self.performance_metrics['flow_table_misses']) > 0:
            hit_ratio = (self.performance_metrics['flow_table_hits'] / 
                        (self.performance_metrics['flow_table_hits'] + self.performance_metrics['flow_table_misses']) * 100)
        
        report = f"""
    Performance Report for {self.name} ({self.controller_type}):
    --------------------------------------------------------
    Average packet processing time: {avg_processing_time:.2f} ms
    Flow table hits: {self.performance_metrics['flow_table_hits']}
    Flow table misses: {self.performance_metrics['flow_table_misses']}
    Controller requests: {self.performance_metrics['controller_requests']}
    Hit ratio: {hit_ratio:.2f}%
        """
        return report

# Class to compare different SDN controllers
class SDNBenchmark:
    
    def __init__(self):
        self.controllers = {}
        self.results = {}
        
# Function to add a controller to the benchmark
    def add_controller(self, controller):

        self.controllers[controller.name] = controller
        print(f"Added {controller.name} to benchmark")

# Function to generate test network patterns
    def generate_test_traffic(self, num_packets=1000):

        traffic = []
        
        # Generate some HTTP traffic (port 80)
        for i in range(int(num_packets * 0.4)):  # 40% HTTP
            src_ip = f"10.0.0.{random.randint(1, 254)}"
            dst_ip = f"10.0.0.{random.randint(1, 254)}"
            traffic.append({
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': random.randint(1024, 65535),
                'dst_port': 80,
                'protocol': 'TCP'
            })
            
        # Generate some HTTPS traffic (port 443)
        for i in range(int(num_packets * 0.3)):  # 30% HTTPS
            src_ip = f"10.0.0.{random.randint(1, 254)}"
            dst_ip = f"10.0.0.{random.randint(1, 254)}"
            traffic.append({
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': random.randint(1024, 65535),
                'dst_port': 443,
                'protocol': 'TCP'
            })
            
        # Generate some DNS traffic (port 53)
        for i in range(int(num_packets * 0.2)):  # 20% DNS
            src_ip = f"10.0.0.{random.randint(1, 254)}"
            dst_ip = f"10.0.0.{random.randint(1, 254)}"
            traffic.append({
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': random.randint(1024, 65535),
                'dst_port': 53,
                'protocol': 'UDP'
            })
            
        # Generate some other traffic
        for i in range(int(num_packets * 0.1)):  # 10% other
            src_ip = f"10.0.0.{random.randint(1, 254)}"
            dst_ip = f"10.0.0.{random.randint(1, 254)}"
            traffic.append({
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': random.randint(1024, 65535),
                'dst_port': random.randint(1, 1023),
                'protocol': random.choice(['TCP', 'UDP'])
            })
            
        return traffic
    
# Function to run the benchmark on all the active controllers
    def run_benchmark(self, traffic=None, switch_id="sw1"):
        if traffic is None:
            traffic = self.generate_test_traffic()
            
        print(f"Running benchmark with {len(traffic)} packets...")
        
        for name, controller in self.controllers.items():
            print(f"\nTesting controller: {name}")
            
            # Process all packets
            for packet in traffic:
                controller.process_packet(switch_id, packet)
                
            # Store results
            avg_time = sum(controller.performance_metrics['packet_processing_time']) / len(controller.performance_metrics['packet_processing_time'])
            self.results[name] = {
                'avg_processing_time': avg_time,
                'flow_table_hits': controller.performance_metrics['flow_table_hits'],
                'flow_table_misses': controller.performance_metrics['flow_table_misses'],
                'controller_requests': controller.performance_metrics['controller_requests']
            }
            
            print(controller.get_performance_report())
            
        return self.results

# Function to visualize and plot the benchmark results
    def visualize_results(self):

        if not self.results:
            print("No benchmark results to visualize")
            return
            
        # Plot average processing time
        names = list(self.results.keys())
        avg_times = [self.results[name]['avg_processing_time'] for name in names]
        hits = [self.results[name]['flow_table_hits'] for name in names]
        misses = [self.results[name]['flow_table_misses'] for name in names]
        
        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot average processing time
        ax1.bar(names, avg_times)
        ax1.set_title('Average Packet Processing Time')
        ax1.set_ylabel('Time (ms)')
        ax1.set_xlabel('Controller')
        
        # Plot hit/miss ratio
        width = 0.35
        x = np.arange(len(names))
        ax2.bar(x - width/2, hits, width, label='Hits')
        ax2.bar(x + width/2, misses, width, label='Misses')
        ax2.set_title('Flow Table Hit/Miss Ratio')
        ax2.set_xticks(x)
        ax2.set_xticklabels(names)
        ax2.set_ylabel('Count')
        ax2.set_xlabel('Controller')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('sdn_benchmark_results.png')
        print("Results visualized and saved to 'sdn_benchmark_results.png'")

# Function to implement different SDN architectures
def sdn_architectures():
    print("Different SDN Architectures")
    
    # Create an openflow controller
    controller_openflow = SDNController("OpenFlow-Controller", "OpenFlow")
    controller_openflow.start()
    controller_openflow.add_switch("sw1", 4)
    controller_openflow.add_switch("sw2", 4)
    controller_openflow.add_connection("sw1", "sw2")
    
    # Basic flow rules
    controller_openflow.add_flow_rule("sw1", 
                            {"dst_port": 80}, 
                            {"forward_port": 1})
    controller_openflow.add_flow_rule("sw1", 
                            {"dst_port": 443}, 
                            {"forward_port": 2})

    # Backup Traffic Rules
    controller_openflow.add_flow_rule("sw1", 
                            {"src_ip": "10.0.0.10", "src_port": 2049}, 
                            {"forward_port": 4})
    
    # Create P4-Controller
    controller_p4 = SDNController("P4-Controller", "P4")
    controller_p4.start()
    controller_p4.add_switch("sw1", 4)
    controller_p4.add_switch("sw2", 4)
    controller_p4.add_connection("sw1", "sw2")
    
    # Rules for data plane programming
    controller_p4.add_flow_rule("sw1", 
                            {"protocol": "TCP", "dst_port": 80}, 
                            {"modify": {"qos_priority": "high"}, "forward_port": 1})
    controller_p4.add_flow_rule("sw1", 
                            {"protocol": "UDP"}, 
                            {"forward_port": 3})
    # Rules for backup traffic 
    controller_p4.add_flow_rule("sw1", 
                            {"src_ip": "10.0.0.10", "src_port": 2049}, 
                            {"modify": {"qos_priority": "low"}, "forward_port": 4})
    
    return controller_openflow, controller_p4

# Function to compare two SDN controllers
def compare_sdn_controllers(controller1, controller2):
    print("SDN Controller Comparison")
    
    # Create benchmark class
    benchmark = SDNBenchmark()
    
    # Add controllers to benchmark
    benchmark.add_controller(controller1)
    benchmark.add_controller(controller2)
    
    # Run benchmark
    benchmark.run_benchmark()
    
    # Visualize results
    benchmark.visualize_results()
    
    return benchmark

# Function to evaluate the network performance
def evaluate_network_performance(controller):
    print("SDN Network Performance Evaluation")
    
    # Generate different types of traffic patterns
    traffic_patterns = {
        "web_heavy": [],  # 70% web traffic
        "mixed": [],      # Even mix of traffic
        "backup": []      # Large data transfers
    }
    
    # Web-heavy traffic
    for i in range(700):
        traffic_patterns["web_heavy"].append({
            'src_ip': f"10.0.0.{random.randint(1, 254)}",
            'dst_ip': f"10.0.0.{random.randint(1, 254)}",
            'src_port': random.randint(1024, 65535),
            'dst_port': random.choice([80, 443]),
            'protocol': 'TCP'
        })
    
    for i in range(300):
        traffic_patterns["web_heavy"].append({
            'src_ip': f"10.0.0.{random.randint(1, 254)}",
            'dst_ip': f"10.0.0.{random.randint(1, 254)}",
            'src_port': random.randint(1024, 65535),
            'dst_port': random.randint(1, 1023),
            'protocol': random.choice(['TCP', 'UDP'])
        })
    
    # Mixed traffic - even spread
    for i in range(1000):
        dst_port = random.choice([80, 443, 22, 25, 53, random.randint(1, 1023)])
        traffic_patterns["mixed"].append({
            'src_ip': f"10.0.0.{random.randint(1, 254)}",
            'dst_ip': f"10.0.0.{random.randint(1, 254)}",
            'src_port': random.randint(1024, 65535),
            'dst_port': dst_port,
            'protocol': 'TCP' if dst_port in [80, 443, 22, 25] else 'UDP'
        })
    
    # Backup traffic - large transfers
    for i in range(1000):
        traffic_patterns["backup"].append({
            'src_ip': "10.0.0.10",  # Backup server
            'dst_ip': f"10.0.0.{random.randint(1, 254)}",
            'src_port': 2049,  # NFS
            'dst_port': random.randint(1024, 65535),
            'protocol': 'TCP',
            'size': random.randint(1, 1500) * 1024  # Large packets
        })
    
    # Process each traffic pattern and collect performance data
    results = {}
    for pattern_name, traffic in traffic_patterns.items():
        print(f"\nTesting with {pattern_name} traffic pattern...")
        
        # Reset performance metrics
        controller.performance_metrics = {
            'packet_processing_time': [],
            'flow_table_hits': 0,
            'flow_table_misses': 0,
            'controller_requests': 0
        }
        
        # Process traffic
        for packet in traffic:
            controller.process_packet("sw1", packet)
        
        # Store results
        if controller.performance_metrics['packet_processing_time']:
            avg_time = sum(controller.performance_metrics['packet_processing_time']) / len(controller.performance_metrics['packet_processing_time'])
        else:
            avg_time = 0
            
        results[pattern_name] = {
            'avg_processing_time': avg_time,
            'flow_table_hits': controller.performance_metrics['flow_table_hits'],
            'flow_table_misses': controller.performance_metrics['flow_table_misses'],
            'controller_requests': controller.performance_metrics['controller_requests']
        }
        
        print(controller.get_performance_report())
    
    # Visualize performance results
    patterns = list(results.keys())
    avg_times = [results[pattern]['avg_processing_time'] for pattern in patterns]
    hits = [results[pattern]['flow_table_hits'] for pattern in patterns]
    misses = [results[pattern]['flow_table_misses'] for pattern in patterns]
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot average processing time
    ax1.bar(patterns, avg_times)
    ax1.set_title('Average Packet Processing Time by Traffic Pattern')
    ax1.set_ylabel('Time (ms)')
    ax1.set_xlabel('Traffic Pattern')
    
    # Plot hit/miss ratio
    width = 0.35
    x = np.arange(len(patterns))
    ax2.bar(x - width/2, hits, width, label='Hits')
    ax2.bar(x + width/2, misses, width, label='Misses')
    ax2.set_title('Flow Table Hit/Miss Ratio by Traffic Pattern')
    ax2.set_xticks(x)
    ax2.set_xticklabels(patterns)
    ax2.set_ylabel('Count')
    ax2.set_xlabel('Traffic Pattern')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('sdn_performance_results.png')
    print("Performance results visualized and saved to 'sdn_performance_results.png'")
    
    return results


# Main function that runs all preivous ones
def run_project_timeline():
    print("SDN")
    
    openflow_controller, p4_controller = sdn_architectures()

    benchmark = compare_sdn_controllers(openflow_controller, p4_controller)
    
    openflow_performance = evaluate_network_performance(openflow_controller)

    p4_performance = evaluate_network_performance(p4_controller)
    

if __name__ == "__main__":
    run_project_timeline()
