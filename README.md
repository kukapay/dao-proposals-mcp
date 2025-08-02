# DAO Proposals MCP

An MCP server that aggregates live governance proposals from major DAOs enabling AI agents to track, analyze, and act on decentralized decision-making in real time, powered by [Snapshot](https://snapshot.box/).

![GitHub License](https://img.shields.io/github/license/kukapay/dao-proposals-mcp) 
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Tools**:
  - `list_spaces`: Fetches a list of up to 10 recent Snapshot spaces, including their IDs, names, and descriptions.
  - `list_proposals`: Retrieves up to 10 recent proposals for a given Snapshot space, including proposal IDs, titles, states, creation dates, and end dates.
  - `get_proposal_details`: Fetches detailed information about a specific proposal, including its title, body, state, choices, scores, and vote counts.
- **Prompt**:
  - `summarize_proposals`: Generates a prompt to summarize recent proposals for a specified Snapshot space, leveraging the `list_proposals` tool.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip for dependency management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kukapay/dao-proposals-mcp.git
   cd dao-proposals-mcp
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. **Installing to Claude Desktop**:

    Install the server as a Claude Desktop application:
    ```bash
    uv run mcp install main.py --name "DAO Proposals"
    ```

    Configuration file as a reference:

    ```json
    {
       "mcpServers": {
           "DAO Proposals": {
               "command": "uv",
               "args": [ "--directory", "/path/to/dao-proposals-mcp", "run", "main.py" ]
           }
       }
    }
    ```
    Replace `/path/to/dao-proposals-mcp` with your actual installation path.
   
## Usage

### Example Interactions

1. **List Available Spaces**:
   - **Prompt**:
     ```plaintext
     Can you show me a list of the most recent Snapshot spaces?
     ```
   - **Output**:
     ```plaintext
     Space ID: ens.eth
     Name: ENS
     About: Ethereum Name Service (ENS) is a decentralized naming system...
     ---
     Space ID: aave.eth
     Name: Aave
     About: Aave is a decentralized lending protocol...
     ---
     ```

2. **List Proposals for a Space**:
   - **Prompt**:
     ```plaintext
     Please list the recent proposals for the ENS DAO (space ID: ens.eth).
     ```
   - **Output**:
     ```plaintext
     Proposal ID: 0x123...
     Title: Proposal to Update ENS Governance
     State: Active
     Created: 2025-07-01 12:00:00
     End: 2025-07-08 12:00:00
     ---
     ```

3. **Get Proposal Details**:
   - **Prompt**:
     ```plaintext
     Can you give me detailed information about the proposal with ID 0x123...?
     ```
   - **Output**:
     ```plaintext
     Proposal ID: 0x123...
     Title: Proposal to Update ENS Governance
     State: Active
     Created: 2025-07-01 12:00:00
     End: 2025-07-08 12:00:00
     Choices: Yes, No
     Scores: [1500, 500]
     Votes: 2000
     ------
     This proposal aims to update the governance structure of ENS...
     ```

4. **Summarize Proposals**:
   - **Prompt**:
     ```plaintext
     Summarize the recent proposals for the DAO with space ID 'ens.eth'.
     ```
   - **Output**:
     ```plaintext
     I'll use the list_proposals tool to fetch the proposals for ens.eth and provide a concise summary of their key points.
     ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

