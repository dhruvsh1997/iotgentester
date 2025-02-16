# IoTTestingApp/utils/iot_generator.py
import simpy
import simpy.rt
import numpy as np
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class IoTDataGenerator:
    def __init__(self, start_second=60.0):
        self.current_second = start_second
        self.columns = [
            'second', 'src', 'dst', 'packetcount', 'src_ratio', 'dst_ratio',
            'src_duration_ratio', 'dst_duration_ratio', 'TotalPacketDuration',
            'TotalPacketLenght', 'src_packet_ratio', 'dst_packet_ratio',
            'DioCount', 'DisCount', 'DaoCount', 'OtherMsg', 'label'
        ]
        
    def generate_single_row(self):
        """Generate one row of IoT traffic data"""
        # Network parameters
        src = random.randint(2, 41)
        dst = random.randint(16, 49)
        packet_count = random.randint(1, 3)
        
        # Generate ratios using beta distribution
        src_ratio = np.clip(np.random.beta(2, 2), 0.3, 1.0)
        dst_ratio = np.clip(np.random.beta(2, 2), 0.3, 1.0)
        
        # Duration ratios
        src_duration = np.clip(np.random.beta(2, 2), 0.01, 1.0)
        dst_duration = np.clip(np.random.beta(2, 2), 0.01, 1.0)
        
        # Packet information
        total_duration = np.random.exponential(0.5)
        total_length = int(np.clip(np.random.normal(100, 30), 26, 200))
        
        # Calculate packet ratios
        src_packet_ratio = np.clip(np.random.beta(2, 2), 0.2, 1.0)
        dst_packet_ratio = np.clip(np.random.beta(2, 2), 0.2, 1.0)
        
        # Message counts
        dio_count = min(np.random.poisson(0.3), 1)
        dis_count = min(np.random.poisson(0.2), 1)
        dao_count = min(np.random.poisson(0.4), 2)
        other_msg = min(np.random.poisson(0.5), 2)
        lbl=np.random.randint(0,2)
        
        return [
            self.current_second, src, dst, packet_count,
            src_ratio, dst_ratio, src_duration, dst_duration,
            total_duration, total_length, src_packet_ratio, dst_packet_ratio,
            dio_count, dis_count, dao_count, other_msg, lbl
        ]

    def plot_traffic_metrics(self, df):
        """Plot various IoT traffic metrics"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Packet counts over time
        ax1.plot(df['second'], df['packetcount'], 'b-')
        ax1.set_title('Packet Count Over Time')
        ax1.set_xlabel('Second')
        ax1.set_ylabel('Packet Count')
        ax1.grid(True)
        
        # Packet length distribution
        ax2.hist(df['TotalPacketLenght'], bins=20, color='green', alpha=0.7)
        ax2.set_title('Packet Length Distribution')
        ax2.set_xlabel('Packet Length')
        ax2.set_ylabel('Frequency')
        ax2.grid(True)
        
        # Network topology
        ax3.scatter(df['src'], df['dst'], alpha=0.5)
        ax3.set_title('Network Traffic Pattern')
        ax3.set_xlabel('Source Node')
        ax3.set_ylabel('Destination Node')
        ax3.grid(True)
        
        # Message type distribution
        message_types = ['DioCount', 'DisCount', 'DaoCount', 'OtherMsg']
        message_counts = [df[col].sum() for col in message_types]
        ax4.bar(message_types, message_counts)
        ax4.set_title('Message Type Distribution')
        ax4.set_ylabel('Count')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Convert plot to base64 string for web display
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(image_png).decode()

class IoTSimulation:
    def __init__(self, env, num_rows, generator):
        self.env = env
        self.num_rows = num_rows
        self.generator = generator
        self.data = []
        self.columns = generator.columns
        
    def generate_traffic(self):
        """SimPy process for generating traffic data"""
        for i in range(self.num_rows):
            row = self.generator.generate_single_row()
            self.data.append(row)
            self.generator.current_second += random.uniform(0.5, 2.0)
            yield self.env.timeout(1)

def generate_iot_data(num_rows, time_factor=1.0):
    """
    Generate IoT traffic data using SimPy simulation
    
    Args:
        num_rows (int): Number of data rows to generate
        time_factor (float): Time scaling factor for simulation
        
    Returns:
        tuple: (DataFrame with generated data, base64 encoded plot image)
    """
    # Create SimPy environment
    env = simpy.rt.RealtimeEnvironment(factor=time_factor, strict=False)
    
    # Initialize generator and simulation
    generator = IoTDataGenerator()
    simulation = IoTSimulation(env, num_rows, generator)
    
    # Start simulation process
    env.process(simulation.generate_traffic())
    
    # Run simulation
    env.run()
    
    # Convert to DataFrame
    df = pd.DataFrame(simulation.data, columns=simulation.columns)
    
    # Generate visualization
    plot_image = generator.plot_traffic_metrics(df)
    
    return df, plot_image