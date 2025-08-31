# Mon Site Flask sur Render

Un petit site web en **Flask** prêt à déployer sur [Render](https://render.com).

## 🚀 Déploiement local
```bash
pip install -r requirements.txt
python app.py
```
Puis ouvre [http://localhost:5000](http://localhost:5000) dans ton navigateur.

## 🌐 Déploiement sur Render
- Connecte ton repo GitHub à Render
- Configure :
  - Build Command : `pip install -r requirements.txt`
  - Start Command : `gunicorn app:app`
