# AWS EC2 Setup Guide - Step by Step

## 🚀 Phase 1: AWS Account & EC2 Instance Setup

### Step 1: Create AWS Account (5 minutes)

1. **Go to AWS:**
   - Visit: https://aws.amazon.com
   - Click **"Create an AWS Account"** (orange button, top right)

2. **Account Details:**
   ```
   Email: your_email@example.com
   Password: Create a strong password
   AWS Account Name: mini-rag-deployment (or your name)
   ```

3. **Contact Information:**
   - Choose **"Personal"** account type
   - Fill in your name, phone, address
   - Click **"Continue"**

4. **Payment Information:**
   - Add credit/debit card (required, but won't be charged if using free tier)
   - AWS will charge ₹2 for verification (refunded immediately)
   - Click **"Verify and Continue"**

5. **Phone Verification:**
   - Enter phone number
   - Choose SMS or voice call
   - Enter verification code
   - Click **"Continue"**

6. **Support Plan:**
   - Select **"Basic Support - Free"**
   - Click **"Complete Sign Up"**

✅ **Account Created!** You'll receive a confirmation email.

---

### Step 2: Set Up Billing Alerts (3 minutes)

**Why:** Avoid surprise charges!

1. **Sign in to AWS Console:**
   - Go to: https://console.aws.amazon.com
   - Sign in with your new account

2. **Navigate to Billing:**
   - Click your account name (top right)
   - Click **"Billing and Cost Management"**

3. **Enable Alerts:**
   - Left sidebar → **"Billing preferences"**
   - Check ✅ **"Receive Billing Alerts"**
   - Click **"Save preferences"**

4. **Create Alert:**
   - Left sidebar → **"Budgets"**
   - Click **"Create budget"**
   - Choose **"Zero spend budget"** (recommended for free tier)
   - OR create custom budget:
     ```
     Budget name: Monthly-Alert
     Budgeted amount: $10
     Email: your_email@example.com
     ```
   - Click **"Create budget"**

✅ **Billing alerts set!** You'll get email if costs exceed threshold.

---

### Step 3: Launch EC2 Instance (15 minutes)

#### 3.1: Navigate to EC2

1. **Go to EC2 Dashboard:**
   - AWS Console → Search "EC2" → Click **"EC2"**
   - OR: https://console.aws.amazon.com/ec2

2. **Choose Region:**
   - Top right corner → Select region closest to you
   - Recommended: **"US East (N. Virginia)"** or **"Asia Pacific (Mumbai)"**

#### 3.2: Launch Instance

1. **Click "Launch Instance"** (orange button)

2. **Name and Tags:**
   ```
   Name: mini-rag-server
   ```

3. **Application and OS Images (AMI):**
   ```
   Quick Start: Ubuntu
   AMI: Ubuntu Server 22.04 LTS (Free tier eligible)
   Architecture: 64-bit (x86)
   ```

4. **Instance Type:**
   ```
   Instance type: t2.medium
   
   Why t2.medium?
   - 2 vCPU, 4 GB RAM
   - Enough for Docker + your app
   - Can downgrade to t2.small later
   
   Note: t2.micro (free tier) has only 1GB RAM - too small for Docker
   ```

5. **Key Pair (Login):**
   - Click **"Create new key pair"**
   ```
   Key pair name: mini-rag-key
   Key pair type: RSA
   Private key format: .pem (for Windows/Mac/Linux)
   ```
   - Click **"Create key pair"**
   - **IMPORTANT:** File downloads automatically - **SAVE IT!**
   - Move to safe location: `C:\Users\YourName\.ssh\mini-rag-key.pem`

6. **Network Settings:**
   - Click **"Edit"** next to Network settings
   
   **Firewall (Security Groups):**
   - Select **"Create security group"**
   ```
   Security group name: mini-rag-sg
   Description: Security group for mini-RAG application
   ```
   
   **Inbound Security Group Rules:**
   
   | Type | Protocol | Port | Source | Description |
   |------|----------|------|--------|-------------|
   | SSH | TCP | 22 | My IP | SSH access |
   | HTTP | TCP | 80 | Anywhere (0.0.0.0/0) | Web access |
   | HTTPS | TCP | 443 | Anywhere (0.0.0.0/0) | Secure web |
   | Custom TCP | TCP | 8001 | Anywhere (0.0.0.0/0) | Backend API |
   | Custom TCP | TCP | 5173 | Anywhere (0.0.0.0/0) | Frontend dev |
   
   **To add each rule:**
   - Click **"Add security group rule"**
   - Select type from dropdown
   - Source: Choose "My IP" for SSH, "Anywhere" for others
   - Click **"Add security group rule"** for next one

7. **Configure Storage:**
   ```
   Size: 30 GiB (Free tier: up to 30 GB)
   Volume type: gp3 (General Purpose SSD)
   Delete on termination: ✅ (checked)
   ```

8. **Advanced Details:**
   - Leave as default (you can skip this section)

9. **Summary:**
   - Review on right sidebar:
     ```
     Number of instances: 1
     Instance type: t2.medium
     Storage: 30 GiB
     ```

10. **Launch!**
    - Click **"Launch instance"** (orange button)
    - Wait 30-60 seconds for instance to start

✅ **Instance Launching!**

---

### Step 4: Get Your Instance Details (2 minutes)

1. **View Instance:**
   - Click **"View all instances"**
   - You'll see your instance with status "Running" (green dot)

2. **Get Public IP:**
   - Click on your instance
   - Bottom panel shows details
   - Find **"Public IPv4 address"** - **COPY THIS!**
   - Example: `54.123.45.67`

3. **Save Instance Details:**
   ```
   Instance ID: i-0abc123def456 (example)
   Public IP: 54.123.45.67 (your actual IP)
   Private IP: 172.31.x.x
   Region: us-east-1 (or your chosen region)
   ```

✅ **EC2 Instance Running!**

---

## 📝 What You Have Now

- ✅ AWS account created
- ✅ Billing alerts configured
- ✅ EC2 instance running (Ubuntu 22.04)
- ✅ Security group configured (ports open)
- ✅ SSH key downloaded (`mini-rag-key.pem`)
- ✅ Public IP address

---

## 🎯 Next Step: Connect to Your Server

**You're ready for Phase 2!** 

I'll help you:
1. Connect via SSH
2. Install Docker
3. Deploy your application

**Ready to continue?** Let me know and I'll guide you through connecting to your EC2 instance!

---

## 💰 Cost Reminder

**Current Setup:**
- t2.medium: ~$0.0464/hour = ~$33/month
- 30 GB storage: ~$3/month
- **Total: ~$36/month**

**Free Tier (First 12 months):**
- 750 hours/month of t2.micro FREE
- 30 GB storage FREE
- 15 GB data transfer FREE

**To use free tier:** Change instance type to t2.micro (but it's very slow for Docker)

**Recommendation:** Use t2.medium for setup/testing, then:
- Stop instance when not using (only pay for storage ~$3/month)
- Or downgrade to t2.small (~$17/month) for production
