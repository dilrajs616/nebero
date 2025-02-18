---

layout: default  
title: "Hardware Requirements for LLM Models"

---

# Project Report

## Goal
Our goal is to make a model that can categorize websites based on their scraped data.

## Challenges
The first problem was that we had non-labelled data. To train our model, we needed a labelled dataset. We initially tried clustering websites based on extracted keywords, but the clusters had too much noise.

## Approaches

### Pre-trained Models for Categorization
We tested two types of models:

- **Fine-tuned models from Hugging Face**: These models are faster, smaller, and require fewer resources. However, they are often trained on specific categories only, limiting their ability to categorize all websites accurately.
- **Open-source LLM models from Ollama**: These models (e.g., Meta Llama, Deepseek V3) are highly accurate but require substantial computational resources.

Ollama is a platform where quantized versions of LLM models are published.

### Models Tested from Hugging Face

We tested the following text classification models:

- **Ali Mazhar Text Classification** (only 15 categories available)
- **Tiabet 2** (only 5 categories available)
- **Fine-Tuned Bart Model** (overfitted on training model)
- **Fine-Tuned Zero Shot** (overfitted on training model)

These models fall into two types:
1. **Pre-defined Category Models**: These models directly classify text into categories but have limited flexibility as they are trained on specific datasets.
2. **Zero-Shot Models**: We define a list of categories, and the model evaluates the text to determine the most probable category.

Example:
```python
sequence_to_classify = "one day I will see the world"
candidate_labels = ['travel', 'cooking', 'dancing']
classifier(sequence_to_classify, candidate_labels)
# Output:
# {'labels': ['travel', 'dancing', 'cooking'],
#  'scores': [0.9938651323318481, 0.0032737774308770895, 0.002861034357920289],
#  'sequence': 'one day I will see the world'}
```

## Final Decision
We decided to use the **Facebook Zero-Shot Model**.

### Challenges with the Facebook Zero-Shot Model
- It requires clean text, but scraped website data contains irrelevant information (e.g., cookie notices).

### Solutions
1. **Facebook Bart Large CNN Model**: Used for text summarization before classification. However, this increased processing time significantly.
2. **Keyword Extraction**: More time-efficient than summarization.

## Testing & Results
We tested 1000 websites using the following categories:

```
['Adult And Dating', 'Advertisements', 'Agriculture', 'Alcohol And Tobacco', 'Articles', 'Astrology', 'Automobiles And Transportation', 'Beauty', 'Biography', 'Blogs And Forums', 'Business', 'Cloudflare', 'Construction', 'Drugs', 'Ecommerce And Shopping', 'Education', 'Entertainment', 'Environment', 'Fashion', 'Finance', 'Food And Beverages', 'Gambling', 'Gaming', 'Government', 'Hacking', 'Health', 'Healthcare', 'Hobbies And Interests', 'Home And Garden', 'Intolerance And Hate', 'Jobs Search', 'Life', 'Logistics', 'Medicine', 'News', 'Non Governmental Organization', 'Parked Domain', 'Personal And Portfolio Website', 'Pets And Animals', 'Politics', 'Pornography', 'Real Estate And Property', 'Religious', 'Research', 'Restaurants And Dining', 'Search Engines', 'Security And Defense', 'Services and Repair', 'Social Media Networking', 'Society And Culture', 'Sports', 'Stock Market', 'Technology', 'Tourism', 'Unknown']
```

### First Iteration Results
- We manually categorized the 1000 websites and found **67.5% accuracy**.
- We discovered additional categories missing from our initial list:

```
['Adult Entertainment', 'Architecture', 'Association', 'Auditons', 'AutoMobile', 'Automation', 'Automobiles', 'Business/Technology', 'Bussiness/Nonprofit', 'Coding', 'Constuction', 'Craked APPS', 'Crypto', 'Cybersecurity', 'Data Security', 'Dating', 'E- Commerce', 'E-Commerce', 'Ecommerce', 'Entertainment/Online Video Streaming', 'Escort Services', 'Food and Beverages', 'Hospitality', 'House Interior', 'INNOVATION/Reseach', 'Insurance', 'Jewellery', 'Legal', 'Lighting/Innovation', 'MARKETING', 'MARKETING/AUTOMATION', 'Manufacor', 'Manufactror', 'Manufactur', 'Manufacture', 'Manufacture and supplier', 'Marketing', 'Media/News', 'Music', 'NGO/Charity', 'News/ Blogs', 'ONLINE TOOLS STORE', 'Online Interview Preparation', 'Online Pdf Convertor', 'Online Store', 'Payments', 'Printing', 'Real Estate', 'Recycleing', 'Redirect To Google', 'Rewards And Coupens', 'SUPPLEMENTS', 'Social Media', 'Startup', 'Stationery Items', 'Techonology', 'Trust & Safety', 'UNCATEGORIZED', 'Visualization/Technology', 'WOOD', 'malicious', 'pharmaceutical']
```

### Second Iteration Results
- After updating the category list and retesting, the model's accuracy improved to **~90%**.
- **Note**: Multilingual websites require translation for better classification.

## AI Models for Improved Accuracy
For better accuracy, we need at least two predictions:
1. **Facebook Zero-Shot Model**
2. **An LLM Model**

### Benefits of LLMs
- Can ignore irrelevant text with better prompting.
- Some are multilingual, eliminating the need for translation.
- High accuracy, even with smaller models.

### Best LLM Model Identified
- **Llama3.1-instruct-405b** was found to be the most capable LLM.

***Note**: This research was conducted before DeepseekV3 was released. A detailed comparison between **Llama3.1 405B and Deepseek V3** is included at the end of the document.

| Category               | Benchmark                        | Llama 3.1 405B | Nemotron 4 340B Instruct | GPT-4 (0125) | GPT-4 Omni | Claude 3.5 Sonnet |
|------------------------|---------------------------------|---------------|-------------------------|--------------|------------|------------------|
| **General**           | MMLU (0-shot, CoT)             | 88.6          | 78.7 (non-CoT)          | 85.4         | 88.7       | 88.3             |
|                        | MMLU PRO (5-shot, CoT)        | 73.3          | 62.7                     | 64.8         | 74.0       | 77.0             |
|                        | IFEval                         | 88.6          | 85.1                     | 84.3         | 85.6       | 88.0             |
| **Code**              | HumanEval (0-shot)             | 89.0          | 73.2                     | 86.6         | 90.2       | 92.0             |
|                        | MBPP EvalPlus (base) (0-shot) | 88.6          | 72.8                     | 83.6         | 87.8       | 90.5             |
| **Math**              | GSM8K (8-shot, CoT)            | 96.8          | 92.3 (0-shot)            | 94.2         | 96.1       | 96.4 (0-shot)    |
|                        | MATH (0-shot, CoT)            | 73.8          | 41.1                     | 64.5         | 76.6       | 71.1             |
| **Reasoning**         | ARC Challenge (0-shot)        | 96.9          | 94.6                     | 96.4         | 96.7       | 96.7             |
|                        | GPOQA (0-shot, CoT)           | 51.1          | -                         | 41.4         | 53.6       | 59.4             |
| **Tool use**          | BFCL                            | 88.5          | 86.5                     | 88.3         | 80.5       | 90.2             |
|                        | Nexus                          | 58.7          | -                         | 50.3         | 56.1       | 45.7             |
| **Long context**      | ZeroSCROLLS/QUALITY            | 95.2          | -                         | 95.2         | 90.5       | 90.5             |
|                        | InfiniteBench/En.MC           | 83.4          | -                         | 72.1         | 82.5       | -                |
|                        | NIH/Multi-needle              | 98.1          | -                         | 100.0        | 100.0      | 90.8             |
| **Multilingual**      | Multilingual MGSM (0-shot)     | 91.6          | -                         | 85.9         | 90.5       | 91.6             |

### Open Source Models and Quantization

The open-source models available to use locally on our systems are always in quantized form.

### **Explanation of Quantization Types**  

Quantization is a technique used to reduce the memory and computational requirements of AI models by representing weights with fewer bits. The different quantization types listed here refer to how the weights are stored and processed. Here’s what they mean:

---

### **1. `fp16` (Full-Precision 16-bit Floating Point)**
   - **Type:** Floating point  
   - **Description:** Uses **16-bit floating-point (FP16)** numbers to represent weights.  
   - **Pros:** Higher precision, better accuracy.  
   - **Cons:** Requires more memory compared to lower-bit quantized models.  
   - **Use Case:** Best for high-performance inference with minimal accuracy loss.  

---

### **2. `q2_K`, `q3_K_L`, `q3_K_M`, `q3_K_S` (2-bit & 3-bit Quantization)**
   - **Type:** Low-bit integer quantization  
   - **Description:**  
     - `q2_K` → **2-bit quantization** (very aggressive compression).  
     - `q3_K_L` → **3-bit quantization (Large variant)**.  
     - `q3_K_M` → **3-bit quantization (Medium variant)**.  
     - `q3_K_S` → **3-bit quantization (Small variant)**.  
   - **Pros:** Very small model size, extremely fast inference.  
   - **Cons:** High accuracy loss compared to higher-bit quantizations.  
   - **Use Case:** Suitable for **edge devices** or applications needing extreme memory efficiency.  

---

### **3. `q4_0`, `q4_1`, `q4_K_M`, `q4_K_S` (4-bit Quantization)**
   - **Type:** Moderate quantization  
   - **Description:**  
     - `q4_0` → **4-bit quantization (basic method, less accurate)**.  
     - `q4_1` → **4-bit quantization (slightly better precision than `q4_0`)**.  
     - `q4_K_M` → **4-bit quantization (Medium variant, optimized for speed/accuracy balance)**.  
     - `q4_K_S` → **4-bit quantization (Small variant, highly compressed)**.  
   - **Pros:** Good balance of speed, compression, and accuracy.  
   - **Cons:** Slight performance drop compared to FP16.  
   - **Use Case:** Ideal for **cloud inference** or situations where **model size matters but accuracy is still important**.  

---

### **4. `q5_0`, `q5_1`, `q5_K_M`, `q5_K_S` (5-bit Quantization)**
   - **Type:** Higher precision quantization  
   - **Description:**  
     - `q5_0` → **5-bit quantization (basic method)**.  
     - `q5_1` → **5-bit quantization (slightly better accuracy than `q5_0`)**.  
     - `q5_K_M` → **5-bit quantization (Medium variant, accuracy-focused)**.  
     - `q5_K_S` → **5-bit quantization (Small variant, optimized for storage)**.  
   - **Pros:** Higher accuracy than 4-bit quantization while keeping good compression.  
   - **Cons:** Slightly more memory usage than 4-bit.  
   - **Use Case:** Useful when **better accuracy is needed but still with compression benefits**.  

---

### **5. `q6_K` (6-bit Quantization)**
   - **Type:** High precision quantization  
   - **Description:**  
     - Uses **6-bit integer weights**, maintaining a strong balance between compression and accuracy.  
   - **Pros:** Very close to FP16 performance while reducing memory usage significantly.  
   - **Cons:** Slightly larger than lower-bit quantizations but much more efficient than FP16.  
   - **Use Case:** **Best for deployment where accuracy is critical but memory is still a concern**.  

---

### **6. `q8_0` (8-bit Quantization)**
   - **Type:** Near full-precision quantization  
   - **Description:**  
     - Uses **8-bit integers** instead of floating-point numbers.  
   - **Pros:**  
     - Minimal accuracy loss compared to FP16.  
     - Faster inference speed.  
     - Lower memory footprint than FP16 but higher than lower-bit quantizations.  
   - **Cons:** Requires more memory than 4-bit or 5-bit quantizations.  
   - **Use Case:** Best for **latency-sensitive applications where accuracy still matters**.  

---

### **Summary of Quantization Types**
| **Quantization Type** | **Bit Size** | **Pros** | **Cons** | **Best Use Case** |
|----------------------|------------|----------|----------|----------------|
| **`fp16`** | 16-bit | High precision, best accuracy | High memory usage | Best for performance-critical tasks |
| **`q2_K`** | 2-bit | Extremely small model size | High accuracy loss | Extreme memory-constrained environments |
| **`q3_K_L/M/S`** | 3-bit | Very efficient | Significant accuracy loss | Edge devices, ultra-low memory use |
| **`q4_0, q4_1, q4_K_M/S`** | 4-bit | Good compression-accuracy tradeoff | Some performance drop | Cloud inference, mobile AI |
| **`q5_0, q5_1, q5_K_M/S`** | 5-bit | Higher accuracy than 4-bit | Slightly larger size | General-purpose AI tasks |
| **`q6_K`** | 6-bit | Almost FP16 accuracy | Slightly higher memory usage | Balanced accuracy vs efficiency |
| **`q8_0`** | 8-bit | Near-FP16 performance, fast | Uses more memory than 4-bit | Latency-sensitive applications |

---

**Q4 is the standard quantisation for all models. We used the q4 quantised version of Llama3 (not 3.1) for testing.**

First we downloaded a dataset of top 1000 websites from github. We were able to scrape 363 websites out of them. These websites were of following domains.

['Energy' 'Motor Vehicles & Parts' 'Wholesalers' 'Technology' 'Financials' 'Retailing' 'Food & Drug Stores' 'Aerospace & Defense' 'Household Products' 'Health Care' 'Food, Beverages & Tobacco' 'Chemicals' 'Industrials' 'Materials' 'Transportation' 'Business Services' 'Media' 'Hotels, Resturants & Leisure' 'Engineering & Construction' 'Apparel' 'Telecommunications']

**We were able to achieve an accuracy of 90 percent. Following were the websites that were categorized incorrectly.**

| Website                            | Category                                  | Industry                          | Sector                                  |
|------------------------------------|-------------------------------------------|-----------------------------------|-----------------------------------------|
| [Dow](http://www.dow.com)          | Business/Industry                        | Chemicals                         | Chemicals                              |
| [Intel](http://www.intel.com)      | International organization               | Technology                        | Semiconductors and Other Electronic Components |
| [CHS Inc](http://www.chsinc.com)   | Company/Enterprise                       | Food, Beverages & Tobacco        | Food Production                        |
| [PMI](http://www.pmi.com)          | Corporate/E-commerce                     | Food, Beverages & Tobacco        | Tobacco                                |
| [Baker Hughes](http://www.bakerhughes.com) | Corporate/Industrial                 | Energy                            | Oil and Gas Equipment, Services       |
| [Northrop Grumman](http://www.northropgrumman.com) | Business/Industry               | Aerospace & Defense              | Aerospace and Defense                 |
| [International Paper](http://www.internationalpaper.com) | International organization | Materials                         | Packaging, Containers                 |
| [Lear](http://www.lear.com)        | Company                                  | Motor Vehicles & Parts           | Motor Vehicles and Parts              |
| [Edison Investor](http://www.edisoninvestor.com) | Investment/Corporate Affairs   | Energy                            | Utilities: Gas and Electric           |
| [Praxair](http://www.praxair.com)  | Industrial/Manufacturing                 | Chemicals                         | Chemicals                              |
| [Liberty Interactive](http://www.libertyinteractive.com) | E-commerce Investment/Finance | Technology                        | Internet Services and Retailing       |
| [Darden](http://www.darden.com)    | Education                                | Hotels, Restaurants & Leisure    | Food Services                         |
| [Reynolds American](http://www.reynoldsamerican.com) | Health/Non-Profit, Business | Food, Beverages & Tobacco        | Tobacco                                |
| [FMC Technologies](http://www.fmctechnologies.com) | Technology/Telecommunications | Energy | Oil and Gas Equipment, Services |
| [CMC](http://www.cmc.com)          | Art/Design Education                     | Materials                         | Metals                                 |
| [NCR](http://www.ncr.com)          | E-commerce Financial Services            | Technology                        | Computers, Office Equipment           |
| [MRC Global](http://www.mrcglobal.com) | Engineering/Manufacturing Business | Energy | Oil and Gas Equipment, Services |
| [J.B. Hunt](http://www.jbhunt.com) | E-commerce                               | Transportation                    | Trucking, Truck Leasing               |
| [Leidos](http://www.leidos.com)    | Government                               | Technology                        | Information Technology Services       |
| [Sonoco](http://www.sonoco.com)    | Business/Economy                         | Materials                         | Packaging, Containers                 |
| [Aleris](http://www.aleris.com)    | Documentation/Tech Support               | Materials                         | Metals                                 |
| [Liberty Media](http://www.libertymedia.com) | Financial/Corporate                | Media                             | Entertainment                         |
| [Mead Johnson](http://www.meadjohnson.com) | Healthcare                          | Food, Beverages & Tobacco        | Food Consumer Products                |
| [Westlake](http://www.westlake.com) | Corporate News Business/Finance         | Chemicals                         | Chemicals                              |
| [Graphic Packaging](http://www.graphicpkg.com) | Software/Design                 | Materials                         | Packaging, Containers                 |
| [Brunswick](http://www.brunswick.com) | Finance                                | Transportation                    | Transportation Equipment              |
| [Darling Ingredients](http://www.darlingii.com) | Environmental/Sustainability      | Food, Beverages & Tobacco        | Food Production                        |
| [Genesis Energy](http://www.genesisenergy.com) | Investment Financial Services    | Energy                            | Pipelines                              |
| [Watsco](http://www.watsco.com)    | Investment/Finance                      | Wholesalers                        | Wholesalers: Diversified              |
| [Xylem](http://www.xyleminc.com)   | Environment                             | Industrials                        | Industrial Machinery                   |
| [Brinks](http://www.brinks.com)    | Finance                                 | Business Services                  | Diversified Outsourcing Services      |
| [Big Heart Pet](http://www.bigheartpet.com) | Animal Welfare                     | Food, Beverages & Tobacco        | Food Consumer Products                |
| [Unisys](http://www.unisys.com)    | Logistics/Business                     | Technology                        | Information Technology Services       |
| [Hyster-Yale](http://www.hyster-yale.com) | Business/Finance Corporation      | Industrials                        | Industrial Machinery                   |
| [Schnitzer Steel](http://www.schnitzersteel.com) | Corporate/Business              | Materials                         | Metals                                 |
| [AOI](http://www.aointl.com)       | Business/Company Information            | Food, Beverages & Tobacco        | Tobacco                                |
| [NewMarket](http://www.newmarket.com) | Company/Corporate Finance         | Chemicals                         | Chemicals                              |
| [Greenbrier](http://www.gbrx.com)  | Company/Employment                      | Transportation                    | Transportation Equipment              |
| [Universal American](http://www.universalamerican.com) | Gaming, Entertainment         | Health Care                       | Health Care: Insurance and Managed Care |


***Note: All the financial/crypto/insurance sites were categorised with 100 percent accuracy.**

**Then we scraped the same 1000 websites that we did with Facebook Zero Shot Model.**

Again the model gave an accuracy of nearly 90 percent accuracy. But the major problem was coming in categorizing pornographic websites.

---

**To make this project completely foolproof, we will apply 3 layers of predictions. First we will categorize a large number of websites using above mentioned models. Then we will make our own model that will be trained on that labelled dataset. Finally with these 3 layers of categorization we will be able to make the whole project extremely accurate.**

---

### **Detailed Hardware & CPU Offloading Table For LLaMA3.1:405B**

| Model | Size | VRAM Requirement (GPU Memory) | RAM Requirement (CPU) | CPU Offloading Potential | Performance Impact |
|--------|------|------------------|-----------------|------------------|------------------|
| **405b-instruct-fp16** | **812GB** | **>800GB** (H100/A100 cluster) | 1.5-2TB | Not recommended | Severe slowdown, not feasible for CPUs |
| **405b-instruct-q2_K** | 149GB | **~160GB** (8x A100 80GB) | 256-320GB | Possible (50-70%) | Heavy latency (5-10x slower) |
| **405b-instruct-q3_K_L** | 213GB | **~220GB** (4-8x A100 80GB) | 320-512GB | Partial (40-60%) | Noticeable latency increase (~4-6x) |
| **405b-instruct-q3_K_M** | 195GB | **~200GB** (4x A100 80GB) | 320GB | Partial (40-60%) | Medium latency impact (~3-5x) |
| **405b-instruct-q3_K_S** | 175GB | **~180GB** (4x A100 80GB) | 256GB | Partial (30-50%) | Moderate slowdown (~3-4x) |
| **405b-instruct-q4_0** | 229GB | **~240GB** (4-8x A100 80GB) | 384GB | Moderate (30-40%) | Increased inference time (~2-3x) |
| **405b-instruct-q4_1** | 254GB | **~260GB** (4-8x A100 80GB) | 512GB | Moderate (30-40%) | Slight slowdown (~2-3x) |
| **405b-instruct-q4_K_M** | 243GB | **~250GB** (4-8x A100 80GB) | 512GB | Partial (40-50%) | Acceptable latency (~1.5-2.5x) |
| **405b-instruct-q4_K_S** | 231GB | **~240GB** (4-8x A100 80GB) | 384GB | Moderate (30-40%) | Noticeable but usable (~2-3x) |
| **405b-instruct-q5_0** | 279GB | **~280GB** (4-8x A100 80GB) | 512GB+ | Limited (20-30%) | Mild slowdown (~1.5-2x) |
| **405b-instruct-q5_1** | 305GB | **~320GB** (4-8x A100 80GB) | 512GB+ | Limited (20-30%) | Minor impact (~1.2-1.8x) |
| **405b-instruct-q5_K_M** | 287GB | **~290GB** (4-8x A100 80GB) | 512GB+ | Very limited (10-20%) | Slight latency (~1.1-1.5x) |
| **405b-instruct-q5_K_S** | 279GB | **~280GB** (4-8x A100 80GB) | 512GB | Limited (10-20%) | Small impact (~1.1-1.5x) |
| **405b-instruct-q6_K** | 333GB | **~340GB** (8x A100 80GB) | 768GB+ | Not recommended | Too slow for practical use |
| **405b-instruct-q8_0** | 431GB | **~440GB** (8-16x A100 80GB) | 1TB+ | Not feasible | CPU offloading impractical |

---

We were not able to run Deekseek V3 locally due to hardware limitations and there are not many reliable sources to compare the performance of V3 with Llama3.1. The below mentioned table is taken from official deekseek website.

| **Benchmark (Metric)**               | **DeepSeek V3** | **DeepSeek V2.5** | **Qwen2.5** | **Llama3.1** | **Claude-3.5** | **GPT-4o 0905** |
|--------------------------------------|-----------------|-------------------|-------------|--------------|----------------|-----------------|
| **Architecture**                     | MoE             | MoE               | Dense       | Dense        | -              | -               |
| **# Activated Params**               | 37B             | 21B               | 72B         | 405B         | -              | -               |
| **# Total Params**                   | 671B            | 236B              | 72B         | 405B         | -              | -               |
| **English**                          |                 |                   |             |              |                |                 |
| MMLU (EM)                            | 88.5            | 80.6              | 85.3        | 88.6         | 88.3           | 87.2            |
| MMLU-Redux (EM)                      | 89.1            | 80.3              | 85.6        | 86.2         | 88.9           | 88.0            |
| MMLU-Pro (EM)                        | 75.9            | 66.2              | 71.6        | 73.3         | 78.0           | 72.6            |
| DROP (3-shot F1)                     | 91.6            | 87.8              | 76.7        | 88.7         | 88.3           | 83.7            |
| IF-Eval (Prompt Strict)              | 86.1            | 80.6              | 84.1        | 86.0         | 86.5           | 84.3            |
| GPQA-Diamond (Pass@1)                | 59.1            | 41.3              | 49.0        | 51.1         | 65.0           | 49.9            |
| SimpleQA (Correct)                   | 24.9            | 10.2              | 9.1         | 17.1         | 28.4           | 38.2            |
| FRAMES (Acc.)                        | 73.3            | 65.4              | 69.8        | 70.0         | 72.5           | 80.5            |
| LongBench v2 (Acc.)                  | 48.7            | 35.4              | 39.4        | 36.1         | 41.0           | 48.1            |
| **Code**                             |                 |                   |             |              |                |                 |
| HumanEval-Mul (Pass@1)               | 82.6            | 77.4              | 77.3        | 77.2         | 81.7           | 80.5            |
| LiveCodeBench (Pass@1-COT)           | 40.5            | 29.2              | 31.1        | 28.4         | 36.3           | 33.4            |
| LiveCodeBench (Pass@1)               | 37.6            | 28.4              | 28.7        | 30.1         | 32.8           | 34.2            |
| Codeforces (Percentile)              | 51.6            | 35.6              | 24.8        | 25.3         | 20.3           | 23.6            |
| SWE Verified (Resolved)              | 42.0            | 22.6              | 23.8        | 24.5         | 50.8           | 38.8            |
| Aider-Edit (Acc.)                    | 79.7            | 71.6              | 65.4        | 63.9         | 84.2           | 72.9            |
| Aider-Polyglot (Acc.)                | 49.6            | 18.2              | 7.6         | 5.8          | 45.3           | 16.0            |
| **Math**                             |                 |                   |             |              |                |                 |
| AIME 2024 (Pass@1)                   | 39.2            | 16.7              | 23.3        | 23.3         | 16.0           | 9.3             |
| MATH-500 (EM)                        | 90.2            | 74.7              | 80.0        | 73.8         | 78.3           | 74.6            |
| CNMO 2024 (Pass@1)                   | 43.2            | 10.8              | 15.9        | 6.8          | 13.1           | 10.8            |
| **Chinese**                          |                 |                   |             |              |                |                 |
| CLUEWSC (EM)                         | 90.9            | 90.4              | 91.4        | 84.7         | 85.4           | 87.9            |
| C-Eval (EM)                          | 86.5            | 79.5              | 86.1        | 61.5         | 76.7           | 76.0            |
| C-SimpleQA (Correct)                 | 64.1            | 54.1              | 48.4        | 50.4         | 51.3           | 59.3            |


According to this, deepseek is better than Llama in almost all categories. If we want to run deepseek locally then here are the hardware requirements for it.

| Model        | Checksum          | Size   | GPU Memory Required | RAM Required | CPU Offloading | Performance Impact |
|-------------|------------------|--------|--------------------|--------------|---------------|------------------|
| 671b        | 5da0e2d4a9e0     | 404GB  | 4+ GPUs (A100/H100, 80GB+) | 1TB+  | Limited (Offloading possible) | Slower if offloaded |
| 671b-fp16   | 7770bf5a5ed8     | 1.3TB  | 8+ GPUs (H100, 80GB+) | 2TB+  | Not recommended | Best performance on full GPU load |
| 671b-q4_K_M | 5da0e2d4a9e0     | 404GB  | 4+ GPUs (A100/H100, 80GB+) | 1TB+  | Moderate Offloading | Slower but feasible with CPU offload |
| 671b-q8_0   | 96061c74c1a5     | 713GB  | 6+ GPUs (H100, 80GB+) | 1.5TB+  | Minimal Offloading | Nearly full GPU load recommended |
