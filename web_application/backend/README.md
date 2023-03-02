## To run the application first you need to run the `server-side`
1. Move to server directory
```bash
cd Web_Application/backend/
```
2. Install required dependencies with **requirements.txt** using pip
```bash
pip install -r requirements.txt
```
3. Now, run the sever with **uvicorn**
```bash
python -m uvicorn main:app
```