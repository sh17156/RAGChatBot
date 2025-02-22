from langchain_openai import ChatOpenAI
from langchain_community.llms import DeepInfra
from langchain_community.chat_models import ChatAnthropic
from langchain.schema import SystemMessage, HumanMessage
from typing import List, Dict
import os

class ChatManager:
    """Manages chat interactions and responses with support for multiple LLM providers"""
    
    # Model dictionaries for different providers
    OPENAI_MODELS: Dict[str, Dict] = {
        'gpt-3.5-turbo': {
            'name': 'gpt-3.5-turbo',
            'context_length': 4096,
            'cost_per_1k_tokens': 0.0015
        },
        'gpt-4': {
            'name': 'gpt-4',
            'context_length': 8192,
            'cost_per_1k_tokens': 0.03
        },
        'gpt-4-turbo': {
            'name': 'gpt-4-turbo-preview',
            'context_length': 128000,
            'cost_per_1k_tokens': 0.01
        }
    }
    
    DEEPSEEK_MODELS: Dict[str, Dict] = {
        'deepseek-chat': {
            'name': 'deepseek/deepseek-chat-7b',
            'context_length': 8192,
            'cost_per_1k_tokens': 0.002
        },
        'deepseek-coder': {
            'name': 'deepseek/deepseek-coder-6.7b',
            'context_length': 8192,
            'cost_per_1k_tokens': 0.002
        }
    }
    
    CLAUDE_MODELS: Dict[str, Dict] = {
        'claude-3-opus': {
            'name': 'claude-3-opus-20240229',
            'context_length': 200000,
            'cost_per_1k_tokens': 0.015
        },
        'claude-3-sonnet': {
            'name': 'claude-3-sonnet-20240229',
            'context_length': 200000,
            'cost_per_1k_tokens': 0.003
        }
    }
    
    def __init__(self, provider: str = 'openai', model: str = 'gpt-3.5-turbo'):
        """
        Initialize chat manager with specified provider and model
        
        Args:
            provider (str): LLM provider ('openai', 'deepseek', or 'claude')
            model (str): Model name from the respective provider's dictionary
        """
        self.provider = provider
        self.model = model
        
        # Load guardrails
        with open('guardrails/context.md', 'r') as f:
            self.guardrails = f.read()
        
        # Initialize the appropriate LLM based on provider
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the appropriate LLM based on provider and model"""
        if self.provider == 'openai':
            if self.model not in self.OPENAI_MODELS:
                raise ValueError(f"Invalid OpenAI model. Choose from: {list(self.OPENAI_MODELS.keys())}")
            return ChatOpenAI(
                model_name=self.OPENAI_MODELS[self.model]['name'],
                temperature=0.7
            )
        
        elif self.provider == 'deepseek':
            if self.model not in self.DEEPSEEK_MODELS:
                raise ValueError(f"Invalid DeepSeek model. Choose from: {list(self.DEEPSEEK_MODELS.keys())}")
            return DeepInfra(
                model_id=self.DEEPSEEK_MODELS[self.model]['name'],
                temperature=0.7,
                deepinfra_api_token=os.getenv('DEEPSEEK_API_KEY')
            )
        
        elif self.provider == 'claude':
            if self.model not in self.CLAUDE_MODELS:
                raise ValueError(f"Invalid Claude model. Choose from: {list(self.CLAUDE_MODELS.keys())}")
            return ChatAnthropic(
                model_name=self.CLAUDE_MODELS[self.model]['name'],
                temperature=0.7
            )
        
        else:
            raise ValueError("Invalid provider. Choose from: 'openai', 'deepseek', or 'claude'")

    def get_response(self, query: str, context: List[str]) -> str:
        """Get response from LLM using context"""
        if self.provider == 'deepseek':
            # DeepInfra requires different message format
            prompt = f"{self.guardrails}\n\nContext from documents:\n{context}\n\nQuestion: {query}"
            response = self.llm.invoke(prompt)
            return response
        else:
            messages = [
                SystemMessage(content=f"{self.guardrails}\n\nContext from documents:\n{context}"),
                HumanMessage(content=query)
            ]
            response = self.llm.invoke(messages)
            return response.content
    
    @classmethod
    def get_available_models(cls, provider: str = None) -> Dict:
        """
        Get available models for specified provider or all providers
        
        Args:
            provider (str, optional): Provider name to get models for
            
        Returns:
            Dict: Dictionary of available models
        """
        if provider == 'openai':
            return cls.OPENAI_MODELS
        elif provider == 'deepseek':
            return cls.DEEPSEEK_MODELS
        elif provider == 'claude':
            return cls.CLAUDE_MODELS
        elif provider is None:
            return {
                'openai': cls.OPENAI_MODELS,
                'deepseek': cls.DEEPSEEK_MODELS,
                'claude': cls.CLAUDE_MODELS
            }
        else:
            raise ValueError("Invalid provider. Choose from: 'openai', 'deepseek', or 'claude'") 