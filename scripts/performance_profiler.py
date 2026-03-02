import time
import psutil
import os
from functools import wraps
from datetime import datetime

class PerformanceProfiler:
    def __init__(self):
        self.metrics = []
        self.process = psutil.Process(os.getpid())
        
    def get_memory_usage(self):
        return self.process.memory_info().rss / 1024 / 1024
    
    def get_cpu_percent(self):
        return self.process.cpu_percent(interval=0.1)
    
    def profile_function(self, func_name):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"\n{'='*60}")
                print(f"Profiling: {func_name}")
                print(f"{'='*60}")
                
                mem_before = self.get_memory_usage()
                cpu_before = self.get_cpu_percent()
                start_time = time.time()
                
                result = func(*args, **kwargs)
                
                end_time = time.time()
                mem_after = self.get_memory_usage()
                cpu_after = self.get_cpu_percent()
                
                elapsed = end_time - start_time
                mem_delta = mem_after - mem_before
                
                metric = {
                    'function': func_name,
                    'execution_time': elapsed,
                    'memory_before_mb': mem_before,
                    'memory_after_mb': mem_after,
                    'memory_delta_mb': mem_delta,
                    'cpu_before_pct': cpu_before,
                    'cpu_after_pct': cpu_after,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                self.metrics.append(metric)
                
                print(f"\nPerformance Metrics:")
                print(f"  Execution Time: {elapsed:.2f} seconds")
                print(f"  Memory Usage: {mem_after:.2f} MB (Δ {mem_delta:+.2f} MB)")
                print(f"  CPU Usage: {cpu_after:.1f}%")
                print(f"{'='*60}\n")
                
                return result
            return wrapper
        return decorator
    
    def get_summary(self):
        if not self.metrics:
            return "No metrics collected"
        
        total_time = sum(m['execution_time'] for m in self.metrics)
        max_memory = max(m['memory_after_mb'] for m in self.metrics)
        
        summary = f"""
{'='*60}
PERFORMANCE SUMMARY
{'='*60}
Total Functions Profiled: {len(self.metrics)}
Total Execution Time: {total_time:.2f} seconds
Peak Memory Usage: {max_memory:.2f} MB

Detailed Breakdown:
"""
        for metric in self.metrics:
            summary += f"""
  {metric['function']}:
    Time: {metric['execution_time']:.2f}s
    Memory: {metric['memory_after_mb']:.2f} MB (Δ {metric['memory_delta_mb']:+.2f} MB)
    CPU: {metric['cpu_after_pct']:.1f}%
"""
        
        summary += f"{'='*60}\n"
        return summary
    
    def save_metrics(self, filename='../data/performance_metrics.csv'):
        import pandas as pd
        df = pd.DataFrame(self.metrics)
        df.to_csv(filename, index=False)
        print(f"Performance metrics saved to {filename}")
    
    def plot_metrics(self):
        import pandas as pd
        import matplotlib.pyplot as plt
        
        df = pd.DataFrame(self.metrics)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        axes[0, 0].barh(df['function'], df['execution_time'])
        axes[0, 0].set_xlabel('Time (seconds)')
        axes[0, 0].set_title('Execution Time by Function')
        
        axes[0, 1].barh(df['function'], df['memory_delta_mb'])
        axes[0, 1].set_xlabel('Memory Δ (MB)')
        axes[0, 1].set_title('Memory Usage Change')
        
        axes[1, 0].barh(df['function'], df['cpu_after_pct'])
        axes[1, 0].set_xlabel('CPU %')
        axes[1, 0].set_title('CPU Usage')
        
        axes[1, 1].plot(range(len(df)), df['memory_after_mb'], marker='o')
        axes[1, 1].set_xlabel('Function Call Order')
        axes[1, 1].set_ylabel('Memory (MB)')
        axes[1, 1].set_title('Memory Usage Over Time')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig('../data/performance_profile.png', dpi=300, bbox_inches='tight')
        print("Performance plot saved to ../data/performance_profile.png")
        plt.show()

def main():
    profiler = PerformanceProfiler()
    
    @profiler.profile_function("Data Loading")
    def load_data():
        import pandas as pd
        time.sleep(1)
        return pd.DataFrame({'test': range(1000000)})
    
    @profiler.profile_function("Data Processing")
    def process_data(df):
        time.sleep(0.5)
        return df * 2
    
    @profiler.profile_function("Data Analysis")
    def analyze_data(df):
        time.sleep(0.3)
        return df.sum()
    
    print("Starting Performance Profiling Demo...")
    
    data = load_data()
    processed = process_data(data)
    result = analyze_data(processed)
    
    print(profiler.get_summary())
    profiler.save_metrics()
    profiler.plot_metrics()

if __name__ == "__main__":
    main()
