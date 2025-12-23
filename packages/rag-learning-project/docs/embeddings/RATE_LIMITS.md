# Voyage AI Rate Limits

## Current Status

Your Voyage AI account is on the **free tier** with reduced rate limits:
- **3 requests per minute (RPM)**
- **10,000 tokens per minute (TPM)**

## Free Tier Benefits

✅ **200 million free tokens** for Voyage series 3 models  
✅ Perfect for testing and development  
✅ No credit card required to start  

## Upgrading Rate Limits

To unlock standard rate limits, add a payment method:

1. Visit https://dashboard.voyageai.com/
2. Navigate to **Billing** section
3. Add payment method
4. Wait a few minutes for limits to update

### Standard Rate Limits (with payment method)

After adding payment, you'll get:
- **Higher RPM** (varies by plan)
- **Higher TPM** (varies by plan)
- **Still get 200M free tokens** before any charges

## Working with Free Tier Limits

### Best Practices

1. **Add delays between requests**
   ```python
   import time
   
   # Generate embedding
   emb1 = embeddings.embed_query("query 1")
   
   # Wait 20 seconds before next request
   time.sleep(20)
   
   # Generate next embedding
   emb2 = embeddings.embed_query("query 2")
   ```

2. **Use batch processing**
   ```python
   # Instead of multiple single requests
   emb1 = service.embed_document("doc 1")
   emb2 = service.embed_document("doc 2")
   emb3 = service.embed_document("doc 3")
   
   # Use batch (counts as 1 request)
   embs = service.embed_documents_batch([
       "doc 1",
       "doc 2",
       "doc 3"
   ])
   ```

3. **Cache embeddings**
   ```python
   # Store embeddings in database
   # Don't regenerate for same content
   ```

4. **Test with small datasets**
   ```python
   # Start with 10-20 documents
   # Scale up after adding payment method
   ```

## Rate Limit Errors

If you see this error:
```
You have not yet added your payment method in the billing page 
and will have reduced rate limits of 3 RPM and 10K TPM.
```

**Solutions:**
1. Add delays between requests (20+ seconds)
2. Use batch processing
3. Add payment method for higher limits

## Cost After Free Tokens

After using your 200M free tokens:
- **voyage-context-3**: ~$0.12 per 1M tokens

**Example costs:**
- 1,000 job postings: ~$0.07
- 5,000 candidate profiles: ~$0.25
- 10,000 searches: ~$0.03
- **Total: ~$0.35/month**

Very affordable! 💰

## Monitoring Usage

Check your usage at:
https://dashboard.voyageai.com/usage

## Summary

✅ **Free tier is perfect for development**  
✅ **200M free tokens = lots of testing**  
✅ **Add payment method when ready for production**  
✅ **Very affordable pricing after free tokens**  

The implementation is complete and working - you can start using it right away with the free tier!
