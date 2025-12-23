# Setup Checklist - Voyage AI Embeddings

Use this checklist to get your embedding system up and running.

## ✅ Pre-Setup (Already Complete)

- [x] Code implementation complete
- [x] Documentation created
- [x] Test suite ready
- [x] Example scripts prepared
- [x] Dependencies listed in requirements.txt

## 📋 Your Setup Tasks

### Step 1: Install Dependencies

```bash
# Option A: Use setup wizard (recommended)
python setup_embeddings.py

# Option B: Manual installation
pip install voyageai langchain-text-splitters pymongo python-dotenv
```

**Verify:**
```bash
python -c "import voyageai; print('✅ voyageai installed')"
python -c "import langchain_text_splitters; print('✅ langchain-text-splitters installed')"
```

- [ ] Dependencies installed successfully

---

### Step 2: Get Voyage AI API Key

1. Go to https://www.voyageai.com
2. Click "Sign Up" (free account available)
3. Verify your email
4. Navigate to "API Keys" section
5. Click "Create New Key"
6. Copy the API key (starts with `pa-`)

**Important:** Keep your API key secure!

- [ ] Voyage AI account created
- [ ] API key obtained

---

### Step 3: Configure Environment

1. Check if `.env` file exists:
   ```bash
   ls -la .env
   ```

2. If not, create from template:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` file and add your keys:
   ```env
   MONGODB_URI=mongodb+srv://your_username:your_password@cluster.mongodb.net/?retryWrites=true&w=majority
   VOYAGE_API_KEY=pa-your_voyage_api_key_here
   ```

4. Verify configuration:
   ```bash
   # On Windows
   type .env
   
   # On Mac/Linux
   cat .env
   ```

- [ ] `.env` file created
- [ ] `MONGODB_URI` configured
- [ ] `VOYAGE_API_KEY` configured

---

### Step 4: Test the Setup

Run the test suite:

```bash
python tests/integration/test_embeddings.py
```

**Expected Output:**
```
🔑 Testing API Key Configuration...
✅ API key found: pa-xxxxxxxx...

🧪 Testing Embedding Service...
✅ Embedding service initialized
   Testing query embedding...
   ✅ Query embedding generated: dimension=1024

🏢 Testing Job Portal Embeddings...
✅ Job portal embeddings initialized
   ✅ Job embedding generated: dimension=1024
   ✅ Candidate embedding generated: dimension=1024

📊 Testing Embedding Similarity...
   Similarity (Python jobs): 0.8234
   Similarity (Python vs Frontend): 0.4567
   ✅ Similar jobs have higher similarity score

🎉 All tests passed! Embedding system is ready to use.
```

**Troubleshooting:**

If you see "❌ API key not found":
- Check `.env` file exists in project root
- Verify `VOYAGE_API_KEY` is set correctly
- Make sure there are no extra spaces

If you see "❌ Import error":
- Run: `pip install voyageai langchain-text-splitters`

- [ ] All tests passed

---

### Step 5: Run Example

Run the complete example:

```bash
python scripts/demos/example_with_embeddings.py
```

This will:
- Generate real embeddings for job postings
- Generate real embeddings for candidate profiles
- Store them in MongoDB
- Perform vector similarity searches
- Display matching results with scores

**Expected Output:**
```
🚀 Initializing Voyage AI Embedding Service...
📊 Connecting to MongoDB Atlas...

============================================================
EXAMPLE 1: Store Job Posting with Real Embeddings
============================================================
✅ Generated job embedding (dimension: 1024)
   First 5 values: [0.123, -0.456, 0.789, ...]
✅ Stored job posting with ID: 507f1f77bcf86cd799439011

...

✅ All examples completed successfully!
```

- [ ] Example ran successfully
- [ ] Embeddings generated
- [ ] Data stored in MongoDB
- [ ] Search results displayed

---

### Step 6: Verify MongoDB Data

Check your MongoDB Atlas dashboard:

1. Go to https://cloud.mongodb.com
2. Navigate to your cluster
3. Click "Browse Collections"
4. Check `job_portal` database
5. Verify `companies` and `job_seekers` collections have data
6. Check that documents have `requirements_embedding` or `profile_embedding` fields

- [ ] Data visible in MongoDB Atlas
- [ ] Embeddings stored correctly

---

## 🎉 Setup Complete!

If all checkboxes are marked, your embedding system is ready to use!

## 📚 Next Steps

### Immediate

1. **Explore the code**
   - Review `src/job_portal/infrastructure/voyage/embedding_service.py`
   - Check `src/job_portal/services/embeddings/job_portal_embeddings.py`
   - Study `scripts/demos/example_with_embeddings.py`

2. **Read documentation**
   - Quick start: `docs/embeddings/QUICKSTART_EMBEDDINGS.md`
   - Full guide: `docs/embeddings/EMBEDDING_GUIDE.md`
   - Technical details: `docs/embeddings/IMPLEMENTATION_SUMMARY.md`

### Short Term

3. **Update sample data**
   - Regenerate embeddings for existing documents
   - Replace dummy embeddings with real ones

4. **Test search quality**
   - Try different queries
   - Evaluate result relevance
   - Tune parameters if needed

### Medium Term

5. **Integrate with your app**
   - Add embedding generation to your workflow
   - Implement error handling
   - Add caching if needed

6. **Monitor and optimize**
   - Track API usage
   - Monitor costs
   - Optimize batch processing

## 🆘 Need Help?

### Common Issues

**"API key not found"**
- Solution: Check `.env` file in project root
- Verify: `cat .env | grep VOYAGE_API_KEY`

**"Module not found"**
- Solution: `pip install voyageai langchain-text-splitters`

**"Connection refused" (MongoDB)**
- Check MongoDB URI in `.env`
- Verify IP whitelist in Atlas
- Test: `python scripts/maintenance/test_connection.py`

**"Dimension mismatch"**
- Ensure using 1024 dimensions
- Check MongoDB index configuration

### Resources

- **Quick Start**: `docs/embeddings/QUICKSTART_EMBEDDINGS.md`
- **Full Guide**: `docs/embeddings/EMBEDDING_GUIDE.md`
- **Implementation**: `docs/embeddings/EMBEDDING_IMPLEMENTATION.md`
- **Voyage AI Docs**: https://docs.voyageai.com
- **MongoDB Docs**: https://www.mongodb.com/docs/atlas/atlas-vector-search/

### Support Channels

- **Voyage AI**: https://docs.voyageai.com/docs/contact-email
- **MongoDB**: https://www.mongodb.com/docs/atlas/support/

## 📊 Progress Tracking

**Setup Progress:** ___/6 steps completed

**Status:**
- [ ] Not started
- [ ] In progress
- [ ] Complete and tested
- [ ] Production ready

**Date Started:** _______________

**Date Completed:** _______________

---

**Last Updated:** November 27, 2025
