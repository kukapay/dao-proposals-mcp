import asyncio
import httpx
from typing import List
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent, GetPromptResult
from datetime import datetime

SNAPSHOT_API = "https://hub.snapshot.org/graphql"

# Initialize MCP server without lifespan
mcp = FastMCP("DAO Proposals")

def ts2str(ts: int) -> str:
  dt = datetime.fromtimestamp(ts)
  return dt.strftime("%Y-%m-%d %H:%M:%S")

# Tool: List available Snapshot spaces
@mcp.tool()
async def list_spaces(ctx: Context) -> str:
    """
    Fetch a list of available Snapshot spaces.
    
    Parameters:
        None
    
    Returns:
        A formatted string containing space IDs and names.
    """
    query = """
    query Spaces {
      spaces(first: 10, orderBy: "created", orderDirection: desc) {
        id
        name
        about
      }
    }
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SNAPSHOT_API, json={"query": query})
            response.raise_for_status()
            data = response.json()
            spaces = data.get("data", {}).get("spaces", [])
            
            # Format spaces as a readable string
            result = []
            for i, space in enumerate(spaces):
                result.append(
                    f"Space ID: {space['id']}\n"
                    f"Name: {space['name']}\n"
                    f"About: {space['about']}\n"
                    "---"
                )
            return "\n".join(result) if result else "No spaces found"
        except Exception as e:
            return f"Error: {str(e)}"

# Tool: List DAO proposals for a specific space
@mcp.tool()
async def list_proposals(space_id: str, ctx: Context) -> str:
    """
    Fetch a list of recent proposals for a given Snapshot space.
    
    Parameters:
        space_id (str): The unique identifier of the Snapshot space (e.g., 'ens.eth').
    
    Returns:
        A formatted string containing details of up to 10 recent proposals.
    """
    query = """
    query Proposals($space: String!) {
      proposals(first: 10, orderBy: "created", orderDirection: desc, where: { space: $space }) {
        id
        title
        state
        created
        end
      }
    }
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SNAPSHOT_API,
                json={"query": query, "variables": {"space": space_id}}
            )
            response.raise_for_status()
            data = response.json()
            proposals = data.get("data", {}).get("proposals", [])
            
            # Format proposals as a readable string
            result = []
            for i, proposal in enumerate(proposals):
                created_str = ts2str(proposal['created'])
                end_str = ts2str(proposal['end'])
                result.append(
                    f"Proposal ID: {proposal['id']}\n"
                    f"Title: {proposal['title']}\n"
                    f"State: {proposal['state']}\n"
                    f"Created: {created_str}\n"
                    f"End: {end_str}\n"
                    "---"
                )
            return "\n".join(result) if result else "No proposals found"
        except Exception as e:
            return f"Error: {str(e)}"

# Tool: Fetch detailed information about a specific proposal
@mcp.tool()
async def get_proposal_details(proposal_id: str, ctx: Context) -> str:
    """
    Fetch detailed information for a specific proposal.
    
    Parameters:
        proposal_id (str): The unique identifier of the proposal.
    
    Returns:
        A formatted string containing detailed information about the proposal.
    """
    query = """
    query Proposal($id: String!) {
      proposal(id: $id) {
        id
        title
        body
        state
        created
        end
        choices
        scores
        votes
      }
    }
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SNAPSHOT_API,
                json={"query": query, "variables": {"id": proposal_id}}
            )
            response.raise_for_status()
            data = response.json()
            proposal = data.get("data", {}).get("proposal")
            
            if not proposal:
                return "Proposal not found"
            
            created_str = ts2str(proposal['created'])
            end_str = ts2str(proposal['end'])
            return (
                f"Proposal ID: {proposal['id']}\n"
                f"Title: {proposal['title']}\n"
                f"State: {proposal['state']}\n"
                f"Created: {created_str}\n"
                f"End: {end_str}\n"
                f"Choices: {', '.join(proposal['choices'])}\n"
                f"Scores: {proposal['scores']}\n"
                f"Votes: {proposal['votes']}\n"
                "------\n"                
                f"{proposal['body']}"
            )
        except Exception as e:
            return f"Error: {str(e)}"

# Prompt: Generate a summary of DAO proposals
@mcp.prompt()
def summarize_proposals(space_id: str) -> List[PromptMessage]:
    """
    Generate a prompt to summarize proposals for a given space.
    
    Parameters:
        space_id (str): The unique identifier of the Snapshot space.
    
    Returns:
        A list of prompt messages to guide the summarization process.
    """
    return [
        PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Please summarize the recent proposals for the DAO with space ID '{space_id}'. Use the list_proposals tool to fetch the proposal data."
            )
        ),
        PromptMessage(
            role="assistant",
            content=TextContent(
                type="text",
                text="I'll use the list_proposals tool to fetch the proposals and provide a concise summary of their key points."
            )
        )
    ]

# Main execution
if __name__ == "__main__":
    mcp.run()
