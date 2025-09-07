# tools/agent_caller.py
"""
Tool: agent_caller
Description: Call another agent from within an agent. Allows for agent-to-agent communication and delegation of tasks.

CLI Test:
    cd /path/to/oneshot
    python3 -c "
from tools.agent_caller import agent_caller
result = agent_caller('web_agent', 'Find the latest news about AI')
print(result)
"
"""
# Tool that allows agents to call other agents using the existing infrastructure

import subprocess
import json
import os
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List
from app.tool_services import *

TOOL_METADATA = {
    "type": "function",
    "function": {
        "name": "agent_caller",
        "description": "Call another agent to delegate tasks and enable agent-to-agent workflows. This tool allows you to invoke specialist agents and pass them messages and files as context to perform their tasks. Returns the agent's response with execution metadata. Perfect for orchestrating multi-agent workflows where different agents handle different aspects of a task.",
        "parameters": {
            "type": "object",
            "properties": {
                "agent_name": {
                    "type": "string", 
                    "description": "Name of the agent to call. The list_agents tool can be used to show all of the available agents."
                },
                "message": {
                    "type": "string",
                    "description": "A clear instruction or question to send to the target agent. Be specific about *what* you want the agent to accomplish but trust that they know *how* to do it. The agent will receive this message and execute their specialised tools to complete the task."
                },
                "run_id": {
                    "type": "string",
                    "description": "Optional run ID to continue an existing conversation with the target agent. Use this to maintain context across multiple calls to the same agent, allowing for follow-up questions or multi-step workflows.",
                    "default": None
                },
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of file paths to pass as context to the delegated agent. The agent will be able to read the full content of these files and can use them in their task execution. Useful for passing outputs from previous agent calls or providing reference materials.",
                    "default": []
                },
                "urls": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of URLs to pass as context to the delegated agent. The agent will be able to access these web resources and can use them in their task execution. Useful for passing web-based media content (images, documents, etc.) for multimodal processing.",
                    "default": []
                }
            },
            "required": ["agent_name", "message"]
        }
    }
}

def agent_caller(
    agent_name: str, 
    message: str, 
    run_id: Optional[str] = None,
    files: List[str] = None,
    urls: List[str] = None
) -> str:
    """
    Call another agent from within an agent execution context.
    
    This tool enables agent-to-agent communication by:
    1. Using the existing agent runner infrastructure
    2. Managing run continuity if run_id is provided
    3. Passing file context between agents
    4. Maintaining proper isolation between agent calls
    5. Providing detailed metadata about the call
    """
    
    if files is None:
        files = []
    if urls is None:
        urls = []
    
    try:
        # Get project root (where the 'agent' bash script is located)
        project_root = Path(__file__).parent.parent
        agent_script = project_root / "app" / "oneshot"
        
        if not agent_script.exists():
            return json.dumps({
                "success": False,
                "error": "Agent script not found. This tool requires the 'oneshot' bash script to be present.",
                "agent_name": agent_name,
                "call_id": str(uuid.uuid4())[:8]
            }, indent=2)
        
        # Prepare the enhanced message with file contents and URLs
        enhanced_message = message
        
        # Add file contents if files are provided
        if files:
            file_contents = []
            for file_path in files:
                try:
                    file_path_obj = Path(file_path)
                    if file_path_obj.exists():
                        content = read(str(file_path))
                        file_contents.append(f"=== FILE: {file_path} ===\n{content}\n")
                    else:
                        file_contents.append(f"=== FILE: {file_path} ===\n[FILE NOT FOUND]\n")
                except Exception as e:
                    file_contents.append(f"=== FILE: {file_path} ===\n[ERROR READING FILE: {e}]\n")
            
            if file_contents:
                enhanced_message += f"\n\nFILE CONTEXT:\n{''.join(file_contents)}"
        
        # Add URL context if URLs are provided
        if urls:
            url_context = []
            for url in urls:
                url_context.append(f"=== URL: {url} ===")
            
            if url_context:
                enhanced_message += f"\n\nURL CONTEXT:\n{chr(10).join(url_context)}"
        
        # Build command
        cmd = ["bash", str(agent_script), agent_name, enhanced_message]
        
        # Add run-id if provided (assuming the agent script supports it)
        if run_id:
            cmd.extend(["--run-id", run_id])
        
        # Generate a unique call ID for tracking this specific agent-to-agent call
        call_id = str(uuid.uuid4())[:8]
        
        # Execute the agent call
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=300  # 5 minute timeout to prevent hanging
        )
        
        # Process the result
        if result.returncode == 0:
            agent_response = result.stdout.strip()
            
            # Try to extract usage statistics if present (they're usually at the end)
            lines = agent_response.split('\n')
            usage_info = {}
            clean_response = agent_response
            
            # Look for usage statistics in the last few lines
            for i, line in enumerate(reversed(lines[-5:])):
                if "Usage:" in line or "Tools used:" in line:
                    # Found usage info, split the response
                    split_point = len(lines) - 5 + i
                    clean_response = '\n'.join(lines[:split_point]).strip()
                    usage_lines = lines[split_point:]
                    
                    # Parse usage info
                    for usage_line in usage_lines:
                        if "Usage:" in usage_line:
                            usage_info["usage"] = usage_line.replace("**Usage:**", "").strip()
                        elif "Tools used:" in usage_line:
                            usage_info["tools_used"] = usage_line.replace("**Tools used:**", "").strip()
                    break
            
            # Save the agent call for audit trail
            call_log = {
                "call_id": call_id,
                "calling_agent": "unknown",  # We don't have context of the calling agent
                "called_agent": agent_name,
                "message": message,
                "files_passed": files,
                "urls_passed": urls,
                "run_id": run_id,
                "response": clean_response,
                "usage": usage_info,
                "success": True,
                "timestamp": llm("What is the current timestamp in ISO format? Just return the timestamp, nothing else.")
            }
            
            # Save call log
            log_result = save(
                json.dumps(call_log, indent=2),
                f"Agent call log: {agent_name}",
                f"agent_call_{call_id}.json"
            )
            
            return json.dumps({
                "success": True,
                "agent_name": agent_name,
                "call_id": call_id,
                "response": clean_response,
                "usage": usage_info,
                "log_file": log_result["filepath"],
                "run_id": run_id
            }, indent=2)
            
        else:
            error_msg = result.stderr.strip()
            
            # If stderr is empty, check stdout for formatted error messages
            if not error_msg:
                stdout_content = result.stdout.strip()
                if stdout_content:
                    # Check for usage limit specific errors
                    if "Agent reached usage limit" in stdout_content:
                        # Save error log
                        error_log = {
                            "call_id": call_id,
                            "calling_agent": "unknown",
                            "called_agent": agent_name,
                            "message": message,
                            "files_passed": files,
                            "urls_passed": urls,
                            "run_id": run_id,
                            "error": stdout_content,
                            "error_type": "usage_limit_exceeded",
                            "success": False,
                            "timestamp": llm("What is the current timestamp in ISO format? Just return the timestamp, nothing else.")
                        }
                        
                        save(
                            json.dumps(error_log, indent=2),
                            f"Agent call error log: {agent_name}",
                            f"agent_call_error_{call_id}.json"
                        )
                        
                        return json.dumps({
                            "success": False,
                            "error": f"USAGE_LIMIT_EXCEEDED: Agent '{agent_name}' reached its usage limit",
                            "error_type": "usage_limit_exceeded",
                            "details": stdout_content,
                            "agent_name": agent_name,
                            "call_id": call_id,
                            "run_id": run_id,
                            "recovery_suggestions": [
                                f"Continue the agent's work by calling it again with the same run_id: {run_id}",
                                "The agent will get a fresh usage limit allocation for the continuation",
                                "Check the run history for any partial results that were saved",
                                "Consider breaking the task into smaller subtasks if it consistently hits limits"
                            ]
                        }, indent=2)
                    else:
                        error_msg = stdout_content
                else:
                    error_msg = "Unknown error occurred"
            
            # Save error log for other types of errors
            error_log = {
                "call_id": call_id,
                "calling_agent": "unknown",
                "called_agent": agent_name,
                "message": message,
                "files_passed": files,
                "urls_passed": urls,
                "run_id": run_id,
                "error": error_msg,
                "success": False,
                "timestamp": llm("What is the current timestamp in ISO format? Just return the timestamp, nothing else.")
            }
            
            save(
                json.dumps(error_log, indent=2),
                f"Agent call error log: {agent_name}",
                f"agent_call_error_{call_id}.json"
            )
            
            return json.dumps({
                "success": False,
                "error": f"Agent '{agent_name}' execution failed: {error_msg}",
                "agent_name": agent_name,
                "call_id": call_id,
                "run_id": run_id
            }, indent=2)
            
    except subprocess.TimeoutExpired:
        return json.dumps({
            "success": False,
            "error": f"Agent '{agent_name}' call timed out after 5 minutes",
            "agent_name": agent_name,
            "call_id": str(uuid.uuid4())[:8]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to call agent '{agent_name}': {str(e)}",
            "agent_name": agent_name,
            "call_id": str(uuid.uuid4())[:8]
        }, indent=2) 