# Simple Torrent-like Application (STA)

## Overview
This project is a Simple Torrent-like Application (STA) developed for the **Computer Networks** course in Semester 1, 2024-2025. The application mimics a torrent-based file-sharing system and supports multi-direction data transferring (MDDT).

## Features
- **Tracker and Node Architecture**:
  - Centralized tracker that monitors file pieces and nodes.
  - Nodes can request files and inform the tracker about their local repository.
- **Multi-direction Data Transferring (MDDT)**:
  - Download multiple files from multiple source nodes simultaneously.
- **Peer-to-Peer File Sharing**:
  - Supports downloading from multiple peers.
  - Implements uploading (seeding) to other peers.
- **Custom Protocols**:
  - Magnet text and metainfo files for torrent management.
  - Tracker HTTP communication for peer discovery.

## Objectives
- Build a functional torrent-like application with a multithreaded implementation.
- Ensure the application supports concurrent downloads/uploads.
- Provide a user interface for monitoring upload/download statistics.

## Components
1. **Magnet Text**:
   - Contains metadata and a hash code pointing to the metainfo file on the tracker.
2. **Metainfo File (.torrent)**:
   - Includes tracker information, piece length, and piece count.
3. **Pieces**:
   - Uniformly sized parts of a file for downloading (default: 512 KB).
4. **Tracker**:
   - Handles peer registration and provides peer lists.

## Tracker HTTP Protocol
- **Request Parameters**:
  - Magnet text for identifying the metainfo file.
  - Download progress updates (started, stopped, completed).
- **Response Format**:
  - Peer list with details (IP, port, and ID).

## Peer-to-Peer Communication
- **Downloading**:
  - Connect to multiple peers to download file pieces.
  - Maintain a request queue to track progress.
- **Uploading**:
  - Serve file pieces to other peers.
  - Implement seeding strategies.

## User Interface
- Command-line based client supporting fundamental torrent operations.
- Statistics display for uploads and downloads.
- Optional GUI for enhanced visualization.

## Advanced Features
- Distributed Hash Table (DHT) for tracker-less operation.
- Simultaneous torrent management.
- Download/seeding optimization strategies (e.g., rarest-first).
- Tracker scraping for metadata exchange.

## Development Phases
1. **Phase 1** (First 2 weeks):
   - Define application functions and protocols.
   - Submit a softcopy report detailing these definitions.
2. **Phase 2** (Next 2 weeks):
   - Implement and refine the application.
   - Submit a final report including design, source code, and results.

## Evaluation Criteria
- **Tracker Protocol**: 15%
- **Torrent Download**: 30%
- **Torrent Upload**: 15%
- **Multiple Host Deployment**: 20%
- **MDDT Feature**: 10%
- **Advanced Features**: 10%

## Submission Requirements
- **Phase 1 Report**: PDF file containing application functions and protocols.
- **Final Report**: Comprehensive report including all development phases, source code, and application executable.

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/huyhoang8704/CO3093-ComputerNetwork.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tracker:
   ```bash
   python tracker.py
   ```
4. Run the node:
   ```bash
   python node.py
   ```

## Authors
## Team members

| No. | Full name                 | Student ID |
| :-: | --------------------------| :--------: |
| 1   | Nguyễn Huy nHoàng         | 2211091    |
| 2   | Nguyễn Lê Gia Kiệt        | 2211761    |
| 3   | Nguyễn Chí Thiết          | 2213242    |


