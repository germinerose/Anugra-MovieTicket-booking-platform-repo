# 🚀 Quick Start Guide

## Step-by-Step Setup (5 minutes)

### 1. Open Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac**: Press `Cmd + Space`, type `Terminal`, press Enter
- **Linux**: Press `Ctrl + Alt + T`

### 2. Navigate to Project Folder
```bash
cd "D:\Movie Ticket booking Platform"
```

### 3. Create Virtual Environment
```bash
python -m venv venv
```

### 4. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 5. Install Packages
```bash
pip install -r requirements.txt
```

### 6. Add Sample Data (Optional but Recommended)
```bash
python add_sample_data.py
```

This adds 5 sample movies with shows so you can test immediately!

### 7. Run the Application
```bash
python app.py
```

You should see:
```
Database tables created successfully!
 * Running on http://127.0.0.1:5000
```

### 8. Open Browser
Go to: **http://localhost:5000**

## 🎯 First Steps After Launching

1. **Register** a new account
2. **Login** with your credentials
3. **Browse** movies on the home page
4. **Click** "View Shows" on any movie
5. **Select** a show time
6. **Choose** your seats
7. **Book** your tickets!

## ✅ Troubleshooting

**"python is not recognized"**
- Use `python3` instead of `python` (Mac/Linux)
- Make sure Python is installed and added to PATH

**"pip is not recognized"**
- Use `python -m pip` instead of `pip`

**"Port 5000 already in use"**
- Change port in `app.py` line 62: `port=5001`

**"Module not found"**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

## 📚 Next Steps

1. Read `README.md` for detailed documentation
2. Explore the code - each file has comments explaining what it does
3. Try modifying the code to see what happens
4. Add your own movies through the Admin panel

## 💡 Pro Tips

- Keep the terminal window open while the app is running
- Press `Ctrl + C` in terminal to stop the server
- The app auto-reloads when you save code changes (debug mode)
- Check browser console (F12) for JavaScript errors

---

**Happy Coding! 🎬**

