import traceback
from openai import OpenAI
import os
from typing import List, Dict, Any, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer

class AgentClient:
    """
    Client for interacting with LLM API using OpenAI-like interface.
    """
    
    def __init__(self, 
                 api_base: str = "",
                 api_key: Optional[str] = "",
                 model: str = "",
                 temperature: float = 0.7,
                 max_tokens: int = 2048):
        """
        Initialize the AgentClient.
        
        Args:
            api_base: Base URL for the API
            api_key: API key (reads from environment if None)
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in the response
        """
        self.api_base = api_base
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if not self.api_key:
            raise ValueError("API key must be provided either in constructor or as OPENAI_API_KEY environment variable")
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_base)
    

    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Send a chat completion request to the LLM API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
                    (e.g., [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}])

        Returns:
            The assistant's response content as a string, along with token usage information
        """
        response = ""
        prompt_token_length = 0
        completion_token_length = 0
        total_token_length = 0

        # Use infinite retry for qwen3 models
        is_qwen3 = "qwen3" in self.model

        # Check if model name contains "thinking" string
        enable_thinking = is_qwen3 and "-thinking" in self.model.lower()

        # Maximum retry count for non-qwen3 models
        retry_num = 3 if not is_qwen3 else None

        while True:
            try:
                if is_qwen3:
                    if enable_thinking:
                        # Use streaming output to get response with thinking
                        chat_response = self.client.chat.completions.create(
                            model=self.model.removesuffix("-thinking"),
                            messages=messages,
                            temperature=self.temperature,
                            max_tokens=self.max_tokens,
                            stream=True,
                            extra_body={"enable_thinking": True},
                            timeout=300
                        )
                        
                        # Collect complete response
                        full_content = ""
                        usage_info = None
                        
                        for chunk in chat_response:
                            # If there's usage information, save it
                            if hasattr(chunk, 'usage') and chunk.usage:
                                usage_info = chunk.usage
                            
                            # If there's content, add it to response
                            if chunk.choices and chunk.choices[0].delta.content:
                                full_content += chunk.choices[0].delta.content
                        
                        response = full_content.strip()
                        
                        # If there's usage information, update token counts
                        if usage_info:
                            total_token_length += usage_info.total_tokens
                            prompt_token_length += usage_info.prompt_tokens
                            completion_token_length += usage_info.completion_tokens
                    else:
                        # Non-thinking mode qwen3 request
                        chat_response = self.client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            temperature=self.temperature,
                            max_tokens=self.max_tokens,
                            extra_body={"enable_thinking": False},
                            timeout=300
                        )
                        
                        response = chat_response.choices[0].message.content.strip()
                        total_token_length += chat_response.usage.total_tokens
                        prompt_token_length += chat_response.usage.prompt_tokens
                        completion_token_length += chat_response.usage.completion_tokens
                else:
                    # Non-qwen3 model request
                    chat_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        timeout=300
                    )
                    
                    response = chat_response.choices[0].message.content.strip()
                    total_token_length += chat_response.usage.total_tokens
                    prompt_token_length += chat_response.usage.prompt_tokens
                    completion_token_length += chat_response.usage.completion_tokens
                
                # Successfully obtained response, break out of loop
                break
                    
            except Exception as e:
                # For non-qwen3 models, decrease retry count
                if not is_qwen3:
                    retry_num -= 1
                    if retry_num == 0:
                        stack_trace = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                        print(f"<<<<<<Agent Error>>>>>>\n{stack_trace}")
                        break
                # For qwen3 models, log error but continue retrying
                else:
                    # Log retry information
                    stack_trace = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                    print(f"<<<<<<Agent Error>>>>>>\n{stack_trace}")

        print(f"<<<<<<Agent Response>>>>>>\n{response}")
        return response, total_token_length, prompt_token_length, completion_token_length