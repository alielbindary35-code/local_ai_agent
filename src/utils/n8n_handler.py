"""
n8n Workflow Handler
====================

Comprehensive n8n workflow management:
- Workflow creation and management
- Template system for common workflows
- Error handling and logging
- Workflow testing and validation
- API integration
"""

import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from src.utils.api_handler import APIHandler
from src.utils.error_handler import get_error_handler, ErrorCategory
from src.core.paths import get_knowledge_base_dir

logger = logging.getLogger(__name__)
error_handler = get_error_handler()


class N8NHandler:
    """
    Handler for n8n workflow creation and management.
    """
    
    def __init__(
        self,
        n8n_url: str = "http://localhost:5678",
        api_key: Optional[str] = None,
        webhook_url: Optional[str] = None
    ):
        """
        Initialize n8n handler.
        
        Args:
            n8n_url: Base URL of n8n instance
            api_key: n8n API key (if using API authentication)
            webhook_url: Base webhook URL
        """
        self.n8n_url = n8n_url.rstrip('/')
        self.webhook_url = webhook_url or f"{n8n_url}/webhook"
        self.api_handler = APIHandler(base_url=n8n_url, max_retries=3)
        
        if api_key:
            self.api_handler.set_auth_api_key(api_key, 'X-N8N-API-KEY')
        
        # Load workflow templates
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict]:
        """Load workflow templates from knowledge base."""
        templates = {}
        kb_dir = get_knowledge_base_dir() / "n8n"
        
        if kb_dir.exists():
            template_file = kb_dir / "basic_example.json"
            if template_file.exists():
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        templates['basic'] = json.load(f)
                except Exception as e:
                    logger.warning(f"Error loading n8n template: {e}")
        
        return templates
    
    def create_workflow(
        self,
        workflow_name: str,
        workflow_type: str = "basic",
        nodes: Optional[List[Dict]] = None,
        active: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new n8n workflow.
        
        Args:
            workflow_name: Name of the workflow
            workflow_type: Type of workflow template to use
            nodes: Custom nodes (if not using template)
            active: Whether workflow should be active
        
        Returns:
            Dictionary with workflow creation result
        """
        try:
            # Get template or use provided nodes
            if nodes is None:
                if workflow_type in self.templates:
                    template = self.templates[workflow_type]
                    nodes = template.get('nodes', [])
                else:
                    nodes = self._get_default_nodes()
            
            # Create workflow structure
            workflow = {
                'name': workflow_name,
                'nodes': nodes,
                'connections': self._generate_connections(nodes),
                'active': active,
                'settings': {
                    'executionOrder': 'v1'
                },
                'tags': []
            }
            
            # Try to create via API
            if self.api_handler.auth_config:
                response = self.api_handler.post(
                    '/api/v1/workflows',
                    json_data=workflow
                )
                
                if response['success']:
                    logger.info(f"Workflow '{workflow_name}' created via API")
                    return {
                        'success': True,
                        'workflow': response['data'],
                        'workflow_json': workflow,
                        'message': f"Workflow '{workflow_name}' created successfully"
                    }
                else:
                    logger.warning(f"API creation failed: {response.get('error')}")
                    # Fall back to JSON export
                    return {
                        'success': True,
                        'workflow': workflow,
                        'workflow_json': workflow,
                        'message': f"Workflow '{workflow_name}' prepared (API unavailable, use import_n8n_workflow to import)"
                    }
            else:
                # No API key, return workflow JSON for manual import
                return {
                    'success': True,
                    'workflow': workflow,
                    'workflow_json': workflow,
                    'message': f"Workflow '{workflow_name}' prepared (import manually in n8n UI)"
                }
        
        except Exception as e:
            logger.error(f"Error creating workflow: {e}")
            return {
                'success': False,
                'error': str(e),
                'workflow': None
            }
    
    def _get_default_nodes(self) -> List[Dict]:
        """Get default workflow nodes."""
        return [
            {
                'parameters': {},
                'id': 'start',
                'name': 'Start',
                'type': 'n8n-nodes-base.start',
                'typeVersion': 1,
                'position': [250, 300]
            },
            {
                'parameters': {},
                'id': 'end',
                'name': 'End',
                'type': 'n8n-nodes-base.noOp',
                'typeVersion': 1,
                'position': [450, 300]
            }
        ]
    
    def _generate_connections(self, nodes: List[Dict]) -> Dict:
        """Generate connections between nodes."""
        connections = {}
        
        if len(nodes) >= 2:
            # Connect first node to second, etc.
            for i in range(len(nodes) - 1):
                source_id = nodes[i]['id']
                target_id = nodes[i + 1]['id']
                
                if source_id not in connections:
                    connections[source_id] = {}
                
                connections[source_id]['main'] = [[{'node': target_id, 'type': 'main', 'index': 0}]]
        
        return connections
    
    def create_data_processing_workflow(
        self,
        workflow_name: str,
        input_source: str = "webhook",
        output_destination: str = "webhook"
    ) -> Dict[str, Any]:
        """
        Create a data processing workflow template.
        
        Args:
            workflow_name: Name of the workflow
            input_source: Input source type (webhook, file, api)
            output_destination: Output destination type (webhook, file, api)
        
        Returns:
            Workflow creation result
        """
        nodes = [
            {
                'parameters': {},
                'id': 'start',
                'name': 'Start',
                'type': 'n8n-nodes-base.start',
                'typeVersion': 1,
                'position': [250, 300]
            },
            {
                'parameters': {
                    'operation': 'transform'
                },
                'id': 'transform',
                'name': 'Transform Data',
                'type': 'n8n-nodes-base.function',
                'typeVersion': 1,
                'position': [450, 300]
            },
            {
                'parameters': {},
                'id': 'end',
                'name': 'End',
                'type': 'n8n-nodes-base.noOp',
                'typeVersion': 1,
                'position': [650, 300]
            }
        ]
        
        return self.create_workflow(workflow_name, nodes=nodes)
    
    def create_webhook_workflow(
        self,
        workflow_name: str,
        webhook_path: str,
        method: str = "POST"
    ) -> Dict[str, Any]:
        """
        Create a webhook-triggered workflow.
        
        Args:
            workflow_name: Name of the workflow
            webhook_path: Webhook path
            method: HTTP method (GET, POST, etc.)
        
        Returns:
            Workflow creation result
        """
        nodes = [
            {
                'parameters': {
                    'httpMethod': method,
                    'path': webhook_path
                },
                'id': 'webhook',
                'name': 'Webhook',
                'type': 'n8n-nodes-base.webhook',
                'typeVersion': 1,
                'position': [250, 300],
                'webhookId': webhook_path
            },
            {
                'parameters': {},
                'id': 'end',
                'name': 'Respond to Webhook',
                'type': 'n8n-nodes-base.respondToWebhook',
                'typeVersion': 1,
                'position': [450, 300]
            }
        ]
        
        return self.create_workflow(workflow_name, nodes=nodes)
    
    def export_workflow(
        self,
        workflow_id: Optional[str] = None,
        workflow_json: Optional[Dict] = None,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Export workflow to file.
        
        Args:
            workflow_id: Workflow ID (if exporting from API)
            workflow_json: Workflow JSON (if already have it)
            format: Export format (json)
        
        Returns:
            Export result with file path
        """
        try:
            if workflow_json is None and workflow_id:
                # Fetch from API
                response = self.api_handler.get(f'/api/v1/workflows/{workflow_id}')
                if response['success']:
                    workflow_json = response['data']
                else:
                    return {
                        'success': False,
                        'error': f"Failed to fetch workflow: {response.get('error')}"
                    }
            
            if workflow_json is None:
                return {
                    'success': False,
                    'error': 'No workflow data provided'
                }
            
            # Save to file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"n8n_workflow_{timestamp}.json"
            filepath = Path("data") / filename
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(workflow_json, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'filepath': str(filepath),
                'message': f"Workflow exported to {filepath}"
            }
        
        except Exception as e:
            logger.error(f"Error exporting workflow: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def import_workflow(
        self,
        workflow_json: Dict,
        workflow_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Import workflow from JSON.
        
        Args:
            workflow_json: Workflow JSON data
            workflow_name: Optional new name for workflow
        
        Returns:
            Import result
        """
        try:
            if workflow_name:
                workflow_json['name'] = workflow_name
            
            if self.api_handler.auth_config:
                response = self.api_handler.post(
                    '/api/v1/workflows',
                    json_data=workflow_json
                )
                
                if response['success']:
                    return {
                        'success': True,
                        'workflow': response['data'],
                        'message': f"Workflow '{workflow_json.get('name')}' imported successfully"
                    }
                else:
                    return {
                        'success': False,
                        'error': response.get('error', 'Unknown error')
                    }
            else:
                return {
                    'success': True,
                    'workflow': workflow_json,
                    'message': "Workflow prepared (API unavailable, import manually in n8n UI)"
                }
        
        except Exception as e:
            logger.error(f"Error importing workflow: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_webhook(
        self,
        webhook_url: str,
        test_data: Optional[Dict] = None,
        method: str = "POST"
    ) -> Dict[str, Any]:
        """
        Test n8n webhook.
        
        Args:
            webhook_url: Full webhook URL
            test_data: Test data to send
            method: HTTP method
        
        Returns:
            Test result
        """
        try:
            test_handler = APIHandler()
            
            if method.upper() == "POST":
                response = test_handler.post(webhook_url, json_data=test_data or {})
            else:
                response = test_handler.get(webhook_url, params=test_data or {})
            
            return {
                'success': response['success'],
                'status_code': response.get('status_code'),
                'response': response.get('data'),
                'error': response.get('error')
            }
        
        except Exception as e:
            logger.error(f"Error testing webhook: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_workflow_status(
        self,
        workflow_id: str
    ) -> Dict[str, Any]:
        """
        Get workflow status and execution history.
        
        Args:
            workflow_id: Workflow ID
        
        Returns:
            Workflow status information
        """
        try:
            response = self.api_handler.get(f'/api/v1/workflows/{workflow_id}')
            
            if response['success']:
                workflow = response['data']
                return {
                    'success': True,
                    'active': workflow.get('active', False),
                    'name': workflow.get('name'),
                    'nodes_count': len(workflow.get('nodes', [])),
                    'updated_at': workflow.get('updatedAt')
                }
            else:
                return {
                    'success': False,
                    'error': response.get('error')
                }
        
        except Exception as e:
            error_handler.handle_error(
                e,
                context={"workflow_id": workflow_id, "operation": "get_status"},
                category=ErrorCategory.SYSTEM_ERROR
            )
            logger.error(f"Error getting workflow status: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def monitor_workflow_execution(
        self,
        workflow_id: str,
        execution_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Monitor workflow execution and detect failures.
        
        Args:
            workflow_id: Workflow ID
            execution_id: Optional execution ID to monitor
        
        Returns:
            Execution monitoring information
        """
        try:
            if execution_id:
                endpoint = f'/api/v1/executions/{execution_id}'
            else:
                endpoint = f'/api/v1/workflows/{workflow_id}/executions?limit=1'
            
            response = self.api_handler.get(endpoint)
            
            if response['success']:
                execution = response['data']
                if isinstance(execution, list) and execution:
                    execution = execution[0]
                
                return {
                    'success': True,
                    'status': execution.get('finished', False),
                    'mode': execution.get('mode'),
                    'started_at': execution.get('startedAt'),
                    'stopped_at': execution.get('stoppedAt'),
                    'workflow_data': execution.get('workflowData', {})
                }
            else:
                return {
                    'success': False,
                    'error': response.get('error')
                }
        except Exception as e:
            error_handler.handle_error(
                e,
                context={"workflow_id": workflow_id, "operation": "monitor_execution"},
                category=ErrorCategory.SYSTEM_ERROR
            )
            return {
                'success': False,
                'error': str(e)
            }
    
    def validate_workflow(self, workflow_json: Dict) -> Dict[str, Any]:
        """
        Validate workflow structure before creation.
        
        Args:
            workflow_json: Workflow JSON data
        
        Returns:
            Validation result
        """
        validation = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        if 'name' not in workflow_json:
            validation['valid'] = False
            validation['errors'].append('Workflow name is required')
        
        if 'nodes' not in workflow_json:
            validation['valid'] = False
            validation['errors'].append('Workflow nodes are required')
        elif not isinstance(workflow_json['nodes'], list):
            validation['valid'] = False
            validation['errors'].append('Workflow nodes must be a list')
        elif len(workflow_json['nodes']) == 0:
            validation['warnings'].append('Workflow has no nodes')
        
        # Check connections
        if 'connections' not in workflow_json:
            validation['warnings'].append('Workflow has no connections defined')
        
        return validation

