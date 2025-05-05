# 🧠 SDN Controller Simulation in Python

This repository contains a Python-based simulation of **Software-Defined Networking (SDN)** using two controller architectures: **OpenFlow** and **P4**. It evaluates their performance under different network traffic conditions using flow tables, dynamic rule programming, and packet handling.

Developed as a final project for **CS 258 – Software Defined Networking**  
**San Jose State University** | Instructor: Prof. Navrati Saxena  
**Contributors**: Aniket Mishra, Natesh Reddy

---

## 📌 Features

- 🖧 Simulates OpenFlow and P4-based SDN controllers
- 🔁 Adds switches, connections, and flow rules
- 📦 Processes packets and dynamically installs rules
- 📊 Benchmarks flow table performance (hits/misses, processing time)
- 🧪 Evaluates traffic patterns: Web-heavy, Mixed, Backup
- 📈 Generates visual reports (`.png` graphs)

---

## 🏗️ Architecture Overview

- `SDNController`: Core class managing flow tables and packet logic
- `SDNBenchmark`: Runs simulations across controllers
- `evaluate_network_performance()`: Tests traffic pattern performance
- `run_project_timeline()`: Executes complete pipeline and saves results

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/your-username/sdn-controller-simulation-python.git
cd sdn-controller-simulation-python

### 2. Install Dependencies
##### This project uses matplotlib and numpy for visualization and simulation.
pip install matplotlib numpy

### Run the Simulation
`python sdn_simulation.py`

## ✅ What This Project Does

This simulation will:

- ✅ Simulate both **OpenFlow** and **P4** controllers
- ✅ Benchmark them under controlled test conditions
- ✅ Evaluate their performance on three types of traffic patterns:
  - Web-heavy
  - Mixed
  - Backup (large transfers)
- ✅ Save visual outputs to:
  - `sdn_benchmark_results.png`
  - `sdn_performance_results.png`

---

## 📚 References

- **[2]** K. Alghamdi and R. Braun, “Software Defined Network (SDN) and OpenFlow Protocol in 5G Network,” *Communications and Network*, vol. 12, pp. 28–40, 2020.  
  👉 [https://doi.org/10.4236/cn.2020.121002](https://doi.org/10.4236/cn.2020.121002)

- **[5]** J. Hansen, D. E. Lucani, J. Krigslund, M. Medard, and F. H. P. Fitzek, “Network coded software defined networking: Enabling 5G transmission and storage networks,” *IEEE Communications Magazine*, vol. 53, no. 9, pp. 100–107, Sep. 2015.  
  👉 [https://doi.org/10.1109/MCOM.2015.7263352](https://doi.org/10.1109/MCOM.2015.7263352)

- **P4 Consortium**, “P4 tutorials,” GitHub.  
  👉 [https://github.com/p4lang/tutorials](https://github.com/p4lang/tutorials)

- **NOX Repo**, “POX: A Python-based OpenFlow controller,” GitHub.  
  👉 [https://github.com/noxrepo/pox](https://github.com/noxrepo/pox)
