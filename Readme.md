Open Kali Terminal

save the file in any folder 
# 1. Create a virtual environment
python3 -m venv myenv

# 2. Activate the virtual environment
source myenv/bin/activate

# You'll see (myenv) prefix in your terminal prompt
# (myenv) bxf1001g@hostname:~$

# 3. Install packages (e.g., Flask)
pip install flask

# 4. Run the File
python cyber_scanner.py


# 5. In another Terminal run this 
ssh -R 80:localhost:5000 serveo.net

you will see a link copy it and send it to anyone.
