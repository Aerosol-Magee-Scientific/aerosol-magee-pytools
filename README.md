# Aerosol Magee PyTools

Official Python toolkit developed by **Aerosol Magee Scientific (Aerosol d.o.o.)** for real-time data access, processing, and analysis of aerosol instrument data.

This project serves as a **de facto SDK** for Magee Scientific instruments, enabling standardised workflows for data acquisition, validation, and analysis.

---

## 🚀 Features

- 📡 Real-time data access:
  - TCP/IP communication
  - UIDEP protocol

- 📂 Data handling:
  - Instrument file parsing
  - Standardized data structures (pandas DataFrame)

- ✅ QA/QC:
  - Data validation
  - Filtering and flagging

- ⏱️ Processing:
  - Resampling (e.g. hourly averages)
  - Time-series utilities

- 📊 Visualization:
  - Basic plotting
  - Quick-look analysis tools

---

## Project Structure

aerosol_magee_pytools/

├── data_access/            # TCP/IP, UIDEP

├── instruments/          # instrument specific settings

├── examples/    # simplified examples for data access

└── tools/         # shared utilities

## 🤝 Contributing
Contributions are welcome.
Steps:

Fork the repository
Create a new branch
Implement your feature or fix
Submit a Pull Request

Guidelines:

Keep code modular and clean
Follow existing structure
Add tests when applicable

## 🎯 Project Goal
Provide a standardised, reliable, and accessible Python SDK for aerosol instrument data, enabling:

reproducible analysis
consistent QA/QC workflows
seamless integration into scientific environments

## 🏢 About
Developed and maintained by:
Aerosol Magee Scientific
Aerosol d.o.o., Slovenia
📧 mivancic@aerosolmageesci.com


## License

This project is licensed under the Aerosol Magee Scientific Software License.

See the LICENSE file for full terms
