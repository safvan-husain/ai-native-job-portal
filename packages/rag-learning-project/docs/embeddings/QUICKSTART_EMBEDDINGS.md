# Quick Start: Voyage AI Embeddings

Get up and running with real embeddings in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install voyageai langchain-text-splitters
```

Or install everything:
```bash
pip install -r requirements.txt
```

## Step 2: Get API Key

1. Go to [https://www.voyageai.com](https://www.voyageai.com)
2. Sign up for a free account
3. Navigate to **API Keys** in your dashboard
4. Click **Create New Key**
5. Copy your API key

## Step 3: Configure Environment

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your keys:

```env
MONGODB_URI=mongodb+srv://your_connection_string
VOYAGE_API_KEY=pa-your_voyage_api_key_here
```

## Step 4: Test the Setup

```bash
python tests/integration/test_embeddings.py
```

You should see:
```
✅ API key found
✅ Embedding service initialized
✅ Query embedding generated: dimension=1024
✅ Document embedding generated: dimension=1024
🎉 All tests passed!
```

## Step 5: Run Example

```bash
python scripts/demos/example_with_embeddings.py
```

This will:
- Generate real embeddings for job postings
- Generate real embeddings for candidate profiles
- Store them in MongoDB
- Perform vector similarity searches
- Show matching results with scores

## Quick Usage Example

```python
from dotenv import load_dotenv
from job_portal import JobPortalEmbeddings

load_dotenv()

# Initialize
embeddings = JobPortalEmbeddings()

# Generate job posting embedding
job_emb = embeddings.embed_job_posting(
    job_title="Python Developer",
    job_description="Build APIs with Django",
    required_skills=["Python", "Django"],
    experience_level="mid"
)

print(f"Generated embedding with {len(job_emb)} dimensions")
# Output: Generated embedding with 1024 dimensions
```

## What's Next?

1. **Update Sample Data**: Replace dummy embeddings with real ones
   ```bash
   python scripts/maintenance/seed_sample_data.py  # Uses real embeddings if API key is set
   ```

2. **Test Search Quality**: Run searches and evaluate results
   ```bash
   python scripts/demos/example_with_embeddings.py
   ```

3. **Integrate with Your App**: Use the embedding service in your application

## Common Issues

### "API key not found"
- Make sure `.env` file exists in project root
- Check that `VOYAGE_API_KEY` is set correctly
- Restart your Python session after adding the key

### "Module not found: voyageai"
```bash
pip install voyageai
```

### "Connection refused" (MongoDB)
- Check your `MONGODB_URI` in `.env`
- Ensure your IP is whitelisted in MongoDB Atlas
- Verify network connectivity

## Need Help?

- **Full Guide**: See `EMBEDDING_GUIDE.md` for detailed documentation
- **Examples**: Check `scripts/demos/example_with_embeddings.py` for complete examples
- **Voyage AI Docs**: https://docs.voyageai.com
- **MongoDB Docs**: https://www.mongodb.com/docs/atlas/atlas-vector-search/

## Pricing Note

Voyage AI offers:
- **Free tier**: Great for testing and development
- **Pay-as-you-go**: ~$0.12 per 1M tokens

Check current pricing: https://docs.voyageai.com/docs/pricing
