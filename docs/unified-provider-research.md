# Unified API Provider Research

## Summary

Research findings on providers that offer both LLM (Large Language Model) and embedding APIs under a single API key, to replace the current dual OpenRouter/OpenAI setup.

## Provider Comparison

### 1. OpenAI ⭐ **Recommended**
- **LLM Models**: GPT-4, GPT-3.5-turbo, and variants
- **Embedding Models**: text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002
- **Single API Key**: ✅ Yes
- **Pricing**: Pay-as-you-go, competitive
- **Reliability**: Industry-leading uptime
- **Documentation**: Excellent
- **Pros**: 
  - Most mature and stable platform
  - Excellent SDKs and documentation
  - Wide model selection
  - Strong embedding models
- **Cons**: 
  - Not a "model garden" (limited to OpenAI models)
  - Higher cost than some alternatives

### 2. Google AI (Gemini)
- **LLM Models**: Gemini Pro, Gemini Ultra, PaLM 2
- **Embedding Models**: text-embedding-004, embedding-001
- **Single API Key**: ✅ Yes
- **Pricing**: Competitive, free tier available
- **Reliability**: Good (Google Cloud infrastructure)
- **Documentation**: Good
- **Pros**:
  - Free tier for experimentation
  - Fast inference
  - Good embedding models
- **Cons**:
  - Limited model variety compared to model gardens
  - API changes more frequently

### 3. Together AI
- **LLM Models**: Multiple open-source models (Llama, Mistral, etc.)
- **Embedding Models**: Multiple embedding models
- **Single API Key**: ✅ Yes
- **Pricing**: Competitive for open-source models
- **Reliability**: Good
- **Documentation**: Good
- **Pros**:
  - True "model garden" with many open-source options
  - OpenAI-compatible API
  - Good cost for open-source models
- **Cons**:
  - Less mature than OpenAI
  - Model availability can vary

### 4. Azure OpenAI
- **LLM Models**: GPT-4, GPT-3.5, and other OpenAI models
- **Embedding Models**: Same as OpenAI embeddings
- **Single API Key**: ✅ Yes (via Azure credentials)
- **Pricing**: Similar to OpenAI
- **Reliability**: Enterprise-grade
- **Documentation**: Comprehensive
- **Pros**:
  - Enterprise features (VNets, private endpoints)
  - Compliance certifications
  - SLA guarantees
- **Cons**:
  - More complex setup (Azure account required)
  - Additional Azure-specific configuration

### 5. Anyscale (Endpoints)
- **LLM Models**: Multiple open-source models
- **Embedding Models**: Various embedding models
- **Single API Key**: ✅ Yes
- **Pricing**: Competitive
- **Reliability**: Good
- **Documentation**: Good
- **Pros**:
  - OpenAI-compatible API
  - Ray-based infrastructure
  - Good for scaling
- **Cons**:
  - Smaller ecosystem
  - Less well-known

## Self-Hosting Option: Ollama

### Ollama
- **LLM Models**: Llama, Mistral, Mixtral, etc.
- **Embedding Models**: ✅ Supported (nomic-embed-text, etc.)
- **Single API Key**: N/A (self-hosted)
- **Pricing**: Infrastructure cost only
- **Reliability**: Depends on hosting setup
- **Pros**:
  - Full control over models and data
  - No per-request costs
  - Privacy (data stays local)
  - Previous tests showed embeddings worked well
- **Cons**:
  - Previous Fly.io deployment had "very limited success"
  - Requires infrastructure management
  - Higher operational overhead
  - Need to evaluate hosting options further

## Recommendation

**Primary Recommendation: OpenAI**

For immediate implementation, **OpenAI** is the best choice because:

1. **Single API key** for both LLM and embeddings
2. **Proven reliability** and uptime
3. **Excellent embedding models** (text-embedding-3-* series)
4. **Simple integration** with existing OpenAI SDK
5. **No model garden complexity** to manage

**Alternative Recommendation: Together AI**

If a true "model garden" with multiple open-source models is preferred:

1. **Multiple LLM options** from various providers
2. **Multiple embedding models** available
3. **OpenAI-compatible API** for easy migration
4. **Single API key** for all models
5. **Cost-effective** for high-volume use

**Future Consideration: Ollama**

Re-evaluate Ollama for self-hosted embeddings:
- Test on different infrastructure (not just Fly.io)
- Consider hybrid approach (Ollama for embeddings, API for LLM)
- Evaluate cost vs. API services at scale

## Implementation Strategy

### Phase 1: Unified Client Interface
Create an abstract provider interface that supports:
- Text completion/chat
- Text embeddings
- Configuration management
- Error handling

### Phase 2: OpenAI Implementation
Implement OpenAI as the primary provider:
- Use official OpenAI SDK
- Support both async and sync operations
- Comprehensive error handling

### Phase 3: Multi-Provider Support (Optional)
Add support for additional providers:
- Together AI
- Google AI
- Provider factory pattern for easy switching

### Phase 4: Migration Path
- Configuration-based provider selection
- Easy switching between providers
- Backward compatibility considerations

## Security Considerations

- Store API keys in environment variables
- Never commit keys to source code
- Support key rotation
- Implement rate limiting
- Add request logging (without exposing sensitive data)

## Conclusion

Implementing a unified provider client with **OpenAI as the primary provider** satisfies the requirement to consolidate from two API keys to one, while maintaining high quality for both LLM and embedding functionality. The architecture will be flexible enough to support additional providers in the future if needed.
