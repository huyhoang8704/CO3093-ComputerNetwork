# Network Design and Simulation for a Critical Large Hospital

## Overview
This project focuses on designing and simulating a robust and secure network for a large hospital with multiple departments and buildings. The goal is to enable seamless communication and data exchange between different sites using advanced networking technologies. The network is designed and simulated using Cisco Packet Tracer or equivalent software.

## Objectives
- Design a network topology for the hospital’s main and auxiliary sites.
- Enable interaction between different departments and buildings.
- Ensure scalability, high availability, and security.
- Simulate and test the network for performance and reliability.

## Case Study
**Client:** CCC (Computer & Construction Consultant) Agency  
**Scope:** Design a network for the main site (Ho Chi Minh City) and two auxiliary sites (DBP Street and BHTQ Street).  

### Key Requirements:
1. **Main Site:**
   - 2 buildings (A and B) with 5 floors each, equipped with medical devices and workstations.
   - A data center, IT room, and cabling central located separately.
   - Medium-scale setup: 600 workstations, 10 servers, 12+ networking devices.
   - Wired and wireless infrastructure with advanced technologies (e.g., GPON, GigaEthernet).
   - Centralized Internet access via 2xDSL with load balancing.
   - VLAN structure for departmental segmentation.
   - WAN connectivity to auxiliary sites using SD-WAN or MPLS.
   - VPN for site-to-site and remote worker access.

2. **Auxiliary Sites:**
   - Small-scale setup: 260 workstations, 2 servers, 5+ networking devices.
   - WAN connectivity to the main site using leased lines.
   - IT room and cabling central on-site.

3. **General Requirements:**
   - High security with firewalls, IPS/IDS, and phishing detection.
   - Scalability to accommodate a 20% growth in 5 years.
   - Surveillance system integration.

## Steps to Completion
### Step 1: Analyze Requirements
- Survey installation locations.
- Identify high-load areas for optimized device placement.
- Choose a network structure that balances performance and aesthetics.
- Design wireless coverage and network security partitions (e.g., DMZ, server farm).

### Step 2: Equipment and IP Planning
- List equipment with specifications.
- Create a wiring diagram and IP address plan.
- Design WAN connectivity with modern protocols (e.g., SD-WAN, MPLS).

### Step 3: Bandwidth and Throughput Calculation
- Calculate required bandwidth based on workload.
- Propose ISP configurations for hospital needs.

### Step 4: Network Map Simulation
- Use Packet Tracer or GNS3 to design the network map.

### Step 5: Testing
- Test connectivity using tools like ping and traceroute.
- Validate:
  - Intra-VLAN communication.
  - Inter-VLAN communication.
  - Main and auxiliary site connectivity.
  - DMZ server access.
  - Internet access restrictions.

### Step 6: Re-evaluation
- Assess the network’s reliability, security, and ease of upgrade.
- Identify unresolved issues and future development directions.

### Step 7: Submission
- Submit simulation files and project report.

## Advanced Features (Optional)
- Implement security measures: firewalls, ACLs, IDS/ISP.
- Develop a security best practices guide.

## Tools and Technologies
- **Simulation Software:** Cisco Packet Tracer or GNS3.
- **Networking Technologies:** GPON, GigaEthernet, SD-WAN, MPLS.
- **Security Measures:** Firewalls, IPS/IDS, VPN.

## Evaluation Criteria
- Network structure and equipment list: 1 point.
- IP planning and wiring diagram: 1 point.
- Bandwidth and throughput analysis: 1 point.
- Simulation design: 2 points.
- Testing and validation: 2 points.
- Re-evaluation and future orientation: 2 points.
- Simulation file and project report submission: 1 point.

## Submission
- **Deadline:** 4 weeks after assignment release.
- **Format:** Hard copy for presentation and softcopy uploaded to BKeL.

---

**Note:** For detailed testing scenarios and network design examples, refer to the project documentation.
