#!/usr/bin/env python3
"""AMD GPU Monitor - Real-time dashboard"""
import subprocess, time, argparse, json

def get_gpu_info():
    try:
        out = subprocess.check_output(["rocm-smi", "--showtemp", "--showmeminfo", "vram", "--showuse", "--json"], text=True)
        return json.loads(out)
    except:
        return None

def monitor_loop(interval=1):
    print("AMD GPU Monitor (Ctrl+C to stop)")
    print("=" * 60)
    while True:
        info = get_gpu_info()
        if info:
            for gpu_id, data in info.items():
                if "card" in str(gpu_id).lower():
                    temp = data.get("Temperature (Sensor edge) (C)", "N/A")
                    use = data.get("GPU use (%)", "N/A")
                    vram = data.get("VRAM Total Used Memory (B)", "N/A")
                    print(f"GPU {gpu_id}: {temp}°C | Usage: {use}% | VRAM: {int(vram)/1e9:.1f}GB")
        else:
            # Fallback: parse rocm-smi text output
            try:
                out = subprocess.check_output(["rocm-smi"], text=True)
                print(out[:200])
            except:
                print("rocm-smi not available")
        time.sleep(interval)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--interval", type=float, default=1)
    args = p.parse_args()
    monitor_loop(args.interval)
