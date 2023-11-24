import os
from flask import *
from werkzeug.utils import *
from flask_wtf.file import *
import favorites
import image
import user
import post
import requests
import debug
from twilio.rest import *
import pyotp
import random
import urllib.parse
import re
import phonenumbers
from flask_cors import CORS
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from password_generator import PasswordGenerator

pwo = PasswordGenerator()

app = Flask(__name__)
CORS(app)
account_sid = 'ACf14c7783e7a46933669b060745b102ed'
auth_token = os.environ['twilio_auth']
client = Client(account_sid, auth_token)
admin = "+14505210806"

admin_email = os.environ.get('admin_email')
admin_email_psw = os.environ.get('admin_email_psw')


def is_valid_phone_number(phone_number):
  try:
    parsed_number = phonenumbers.parse(phone_number, None)
    return phonenumbers.is_valid_number(parsed_number)
  except phonenumbers.NumberParseException:
    return False


def send_email(email, subject, message_content):
  signature = f"<br><br>Thalia<br>Administrateur<br>Registre des promesses d'achat<br>xi1le7@gmail.com"
  message_content += signature
  msg = MIMEMultipart()
  msg['Subject'] = subject
  msg['From'] = admin_email
  msg['To'] = email
  msg.attach(MIMEText(message_content, 'html'))
  #with open('img.jpg', 'rb') as f:
  #    file_data = f.read()
  #    file_name = f.name
  #img = MIMEImage(file_data, _subtype="jpg")
  #img.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
  #msg.attach(img)
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(admin_email, admin_email_psw)
    smtp.send_message(msg)
  del msg


@app.route('/')
def index():
  if not post.Post.get_all() == []:
    adresse = []
    phone = []
    prixAsk = []
    prixPa = []
    description = []
    idUser = []
    idPost = []
    beforeLiked = []
    liked = []
    shuffled = post.Post.get_all()
    shuffled.reverse()
    #random.shuffle(shuffled)
    for i in shuffled:
      adresse.append(i.adresse)
      phone.append(user.User.get_by_id(i.idUser).phone)
      prixAsk.append("${:,.0f}".format(i.prixAsk))
      prixPa.append("${:,.0f}".format(i.prixPa))
      description.append(i.description)
      idUser.append(i.idUser)
      idPost.append(i.getId())
      if 'phone' and 'password' in session:
        for j in favorites.Favorite.get_all():
          if j.idUserOwner == user.User.get_by_phone(session['phone']).getId():
            beforeLiked.append(j)
        if i.getId() in [j.idPost for j in beforeLiked]:
          liked.append(True)
        else:
          liked.append(False)
      else:
        liked.append(False)
    return render_template('index.html',
                           rows=zip(adresse, phone, prixAsk, prixPa,
                                    description, idUser, idPost, liked))
  else:
    return render_template(
      '404.html',
      message=Markup(
        "Aucune annonce pour l'instant :(<br>Revenez plus tard !"))


@app.route('/createFavorite/<idUserParameter>/<idPostParameter>')
def createFavorite(idUserParameter, idPostParameter):
  if 'phone' and 'password' in session:
    if favorites.Favorite.get_by_idPost_AND_idUserOwner(
        idPostParameter,
        user.User.get_by_phone(session['phone']).getId()) == None:
      fav = favorites.Favorite(
        idPostParameter, idUserParameter,
        user.User.get_by_phone(session['phone']).getId())
      fav.save()
    return redirect(request.referrer + "#section" + idPostParameter)
  else:
    return redirect(url_for('profile'))


@app.route('/createPost')
def createPost():
  if 'phone' and 'password' in session:
    return render_template('createPost.html')
  else:
    return redirect(url_for('profile'))


@app.route('/createPost', methods=['POST'])
def createPostSubmit():
  utilisateur = user.User.get_by_phone(session['phone'])
  annonce = post.Post(utilisateur.getId(), request.form['adresse'],
                      request.form['prixPa'], request.form['prixAsk'],
                      request.form['description'])
  annonce.save()
  tmp = "${:,.0f}".format(int(annonce.prixAsk))
  message_content = f'''Bonjour {utilisateur.firstName.capitalize()},<br>Une nouvelle publication a été ajouté : {annonce.adresse} pour {tmp} de <a href="tel:{utilisateur.phone}">{utilisateur.phone}</a><br><br><a href="https://stripedkeystartup.thabe03.repl.co/">Voir</a><br>Ne pas répondre.'''
  for i in user.User.get_all():
    if not i.phone == utilisateur.phone:
      # message = client.messages.create(
      #     body=message_content,
      #     from_="15672147343",
      #     to= i.phone
      # )
      print(i.phone)
    if not i.email == utilisateur.email:
      send_email(i.email, "Registre des promesses d'achat", message_content)
  alerte = "Annonce ajoutée"
  return redirect(request.referrer)


@app.route('/readFavorites')
def readFavorites():
  if 'phone' and 'password' in session:
    if favorites.Favorite.get_by_userOwner(
        user.User.get_by_phone(session['phone']).getId()) == []:
      return render_template('404.html',
                             message="Aucun favoris pour l'instant :(")
    else:
      adresse = []
      phone = []
      prixAsk = []
      prixPa = []
      description = []
      idUser = []
      idPost = []
      for i in favorites.Favorite.get_by_userOwner(
          user.User.get_by_phone(session['phone']).getId()):
        print(i.idPost)
        adresse.append(post.Post.get_by_id(i.idPost).adresse)
        phone.append(user.User.get_by_id(i.idUser).phone)
        prixAsk.append("${:,.0f}".format(
          post.Post.get_by_id(i.idPost).prixAsk))
        prixPa.append("${:,.0f}".format(post.Post.get_by_id(i.idPost).prixPa))
        description.append(post.Post.get_by_id(i.idPost).description)
        idUser.append(i.idUser)
        idPost.append(i.idPost)
      rows = zip(adresse, phone, prixAsk, prixPa, description, idUser, idPost)
      return render_template('readFavorites.html',
                             rows=rows,
                             idUserOwner=user.User.get_by_phone(
                               session['phone']).getId())
  return redirect(url_for('profile'))


@app.route('/deleteFavorite/<idPostParameter>')
def deleteFavorite(idPostParameter):
  if 'phone' and 'password' in session:
    fav = favorites.Favorite.get_by_idPost_AND_idUserOwner(
      idPostParameter,
      user.User.get_by_phone(session['phone']).getId())
    fav.delete()
    return redirect(request.referrer + "#section" + idPostParameter)
  return redirect(url_for('profile'))


@app.route('/readPostsOwner')
def readPostsOwner():
  if 'phone' and 'password' in session:
    if post.Post.get_by_idUser(
        user.User.get_by_phone(session['phone']).getId()) == []:
      return render_template(
        '404.html',
        message=Markup(
          "Aucune annonce pour l'instant :(<br>Revenez plus tard !"))
    else:
      adresse = []
      prixAsk = []
      prixPa = []
      description = []
      idUser = []
      idPost = []
      for i in post.Post.get_all():
        if i.idUser == user.User.get_by_phone(session['phone']).getId():
          adresse.append(post.Post.get_by_id(i.getId()).adresse)
          prixAsk.append(post.Post.get_by_id(i.getId()).prixAsk)
          prixPa.append(post.Post.get_by_id(i.getId()).prixPa)
          description.append(post.Post.get_by_id(i.getId()).description)
          idUser.append(i.idUser)
          idPost.append(i.getId())
      rows = rows = zip(adresse, prixAsk, prixPa, description, idUser, idPost)
      return render_template('readPostsOwner.html', rows=rows)
  return redirect(url_for('profile'))


@app.route('/readPostsOwner/<idPostParameter>')
def deletePostOwner(idPostParameter):
  if 'phone' and 'password' in session and post.Post.get_by_id(
      idPostParameter).idUser == user.User.get_by_phone(
        session['phone']).getId():
    fav = favorites.Favorite.get_by_idPost(idPostParameter)
    for i in fav:
      i.delete()
    annonce = post.Post.get_by_id(idPostParameter)
    annonce.delete()
    return redirect(request.referrer)
  else:
    return redirect(url_for('profile'))


@app.route('/updatePostOwner', methods=['GET', 'POST'])
def updatePostOwnerSubmit():
  annonce = post.Post.get_by_id(request.form['idPostParameter'])
  annonce.adresse = request.form['adresse']
  annonce.prixAsk = request.form['prixAsk']
  annonce.prixPa = request.form['prixPa']
  annonce.description = request.form['description']
  annonce.update()
  alerte = "Mise à jour pour l'identifiant " + session['phone']
  return redirect(url_for('readPostsOwner', alerte=alerte))


@app.route('/profile')
def profile():
  if 'phone' and 'password' in session:
    return render_template('connexion.html', admin=session['phone'])
  else:
    return render_template('profile.html')


@app.route('/signin')
def signin():
  if 'phone' and 'password' in session:
    return redirect(url_for('profile'))
  else:
    return render_template('signin.html')


@app.route('/phone', methods=['POST'])
def phone():
  session['phone'] = "+" + re.sub(r'\D', '', request.form['phone_number'])
  if not is_valid_phone_number(session['phone']):
    alerte = 'Ce numéro de téléphone est invalide'
    return redirect(url_for('signin', alerte=alerte))
  session['updatePhone'] = None
  utilisateur = user.User.get_by_phone(session['phone'])
  if utilisateur == None:
    alerte = "Ce numéro de téléphone n'est pas enregistré"
    return redirect(url_for('signup', alerte=alerte))
  return redirect(url_for('code'))


@app.route('/phone2', methods=['POST'])
def phone2():
  session['updatePhone'] = [
    "+" + re.sub(r'\D', '', request.form['oldPhone']),
    "+" + re.sub(r'\D', '', request.form['phone_number']),
    request.form['password']
  ]
  session['phone'] = session['updatePhone'][1]
  if not is_valid_phone_number(session['phone']):
    alerte = 'Ce numéro de téléphone est invalide'
    return redirect(url_for('signin', alerte=alerte))
  if user.User.get_by_phone(session['updatePhone'][0]) == None:
    alerte = "Ce numéro de téléphone n'est pas enregistré"
    return redirect(url_for('signup', alerte=alerte))
  if request.form['oldPhone'] == request.form['phone_number']:
    alerte = "Le vieux et le nouveau numéro de téléphone sont identiques"
    return redirect(url_for('updatePhone', alerte=alerte))
  if not user.User.get_by_phone(session['updatePhone'][1]) == None:
    alerte = "Le numéro de téléphone est déjà enregistré"
    return redirect(url_for('updatePhone', alerte=alerte))
  if user.User.get_by_phone(session['updatePhone'][0]) == None:
    alerte = "Ce numéro de téléphone n'est pas enregistré"
    return redirect(url_for('signup', alerte=alerte))
  if not session['updatePhone'][2] == user.User.get_by_phone(
      session['updatePhone'][0]).password:
    alerte = "Le mot de passe est invalide. Veuillez recommencer."
    return redirect(url_for('updatePhone', alerte=alerte))
  return redirect(url_for('code'))


@app.route("/code")
def code():
  if 'phone' and 'password' in session:
    return redirect(url_for('profile'))
  else:
    phone = session['phone']
    totp = pyotp.TOTP(pyotp.random_base32())
    code = totp.now()
    message = client.messages.create(from_='+15672147343',
                                     body="Code de vérification : " + code,
                                     to=phone)
    session['code'] = code
    return render_template('code.html')


@app.route("/code", methods=['POST'])
def codeSubmit():
  if 'phone' and 'password' in session:
    return redirect(url_for('profile'))
  else:
    code = request.form["code_verification"]
    return redirect(url_for('multiplePath', code=code))


@app.route("/multiplePath/<code>")
def multiplePath(code):
  if not session['code'] == code:
    alerte = 'Le code ne correspond pas'
    return redirect(url_for('updatePhone', alerte=alerte))
  if not session['updatePhone'] == None:
    utilisateur = user.User.get_by_phone(session['updatePhone'][0])
    utilisateur.phone = session['phone']
    utilisateur.update()
    session['phone'] = utilisateur.phone
    alerte = "Mise à jour pour l'identifiant " + session['phone']
    session.clear()
    return redirect(url_for('profile', alerte=alerte))
  utilisateur = user.User.get_by_phone(session['phone'])
  session['phone'] = utilisateur.phone
  session['password'] = utilisateur.password
  return redirect(url_for('profile'))


@app.route('/signup')
def signup():
  if 'phone' and 'password' in session:
    return redirect(url_for('profile'))
  elif 'phone' in session:
    return render_template('signup.html')
  else:
    return redirect(url_for('signin'))


@app.route("/signup", methods=['POST'])
def signupSubmit():
  alerte = ""
  if user.User.get_by_phone(session['phone']) == None:
    utilisateur = user.User(request.form['firstName'],
                            request.form['lastName'], request.form['email'],
                            session['phone'], request.form['password'])
    utilisateur.save()
    session['password'] = utilisateur.password
    send_email(
      utilisateur.email, "Abonnement à l'infolettre",
      f"Bonjour {utilisateur.firstName.capitalize()},<br>Bienvenue dans le registre des promesses d'achat<br>Ne pas répondre."
    )
    alerte = 'Bienvenue ' + session['phone']
  else:
    alerte = 'Utilisateur ' + session['phone'] + " existe déjà"
  return redirect(url_for("profile", alerte=alerte))


@app.route('/updateUser')
def updateUser():
  if 'phone' and 'password' in session:
    utilisateur = user.User.get_by_phone(session['phone'])
    return render_template('updateUser.html', utilisateur=utilisateur)
  else:
    return redirect(url_for('profile'))


@app.route('/updateUser', methods=['POST'])
def updateUserSubmit():
  alerte = ""
  utilisateur = user.User.get_by_phone(session['phone'])
  if not request.form['password'] == utilisateur.password:
    alerte = "Le mot de passe est invalide. Veuillez recommencer."
  else:
    utilisateur.firstName = request.form['firstName']
    utilisateur.lastName = request.form['lastName']
    utilisateur.email = request.form['email']
    utilisateur.update()
    alerte = "Mise à jour pour l'identifiant " + session['phone']
  return redirect(url_for('updateUser', alerte=alerte))


@app.route('/deleteUser', methods=['GET', 'POST'])
def deleteUser():
  if 'phone' and 'password' in session:
    utilisateur = user.User.get_by_phone(session['phone'])
    annonces = post.Post.get_by_idUser(utilisateur.getId())
    favs = favorites.Favorite.get_by_userOwner(utilisateur.getId())
    for fav in favs:
      fav.delete()
    for annonce in annonces:
      annonce.delete()
    utilisateur.delete()
    alerte = "Compte " + session['phone'] + " supprimé"
    session.clear()
    return redirect(url_for('profile', alerte=alerte))
  else:
    return redirect(url_for('profile'))


@app.route('/logout')
def logout():
  if 'phone' and 'password' in session:
    session.clear()
  return redirect(url_for('profile'))


@app.route('/admin_readUsers')
def admin_readUsers():
  if session['phone'] == admin and session[
      'password'] == user.User.get_by_phone(admin).password:
    if user.User.get_all() == []:
      return render_template('404.html', message="Aucun utilisateur")
    else:
      firstName = []
      lastName = []
      email = []
      phone = []
      password = []
      idUser = []
      for i in user.User.get_all():
        firstName.append(i.firstName)
        lastName.append(i.lastName)
        email.append(i.email)
        phone.append(i.phone)
        password.append(i.password)
        idUser.append(i.getId())
      rows = zip(firstName, lastName, email, phone, password, idUser)
      return render_template('admin_readUsers.html', rows=rows)
  return redirect(url_for('profile'))


@app.route('/admin_deleteUser/<idUserParameter>')
def admin_deleteUser(idUserParameter):
  if session['phone'] == admin and session[
      'password'] == user.User.get_by_phone(admin).password:
    utilisateur = user.User.get_by_id(idUserParameter)
    annonces = post.Post.get_by_idUser(utilisateur.getId())
    for i in favorites.Favorite.get_by_userOwner(utilisateur.getId()):
      favs = favorites.Favorite.get_by_idPost(i.idPost)
      for fav in favs:
        fav.delete()
    for annonce in annonces:
      annonce.delete()
    utilisateur.delete()
    alerte = "Compte " + session['phone'] + " supprimé"
    return redirect(url_for('admin_readUsers', alerte=alerte))
  else:
    return redirect(url_for('profile'))


@app.route('/updatePhone')
def updatePhone():
  return render_template("updatePhone.html")


@app.route('/updatePassword')
def updatePassword():
  if 'phone' and 'password' in session:
    utilisateur = user.User.get_by_phone(session['phone'])
    session['updatePassword'] = pwo.generate()
    send_email(
      utilisateur.email, "Récupération de mot de passe", "Bonjour " +
      utilisateur.firstName + "<br>Voici votre mot de passe temporaire " +
      session['updatePassword'] + "<br>Ne pas répondre.")
    return render_template("updatePassword.html")
  else:
    return redirect(url_for('profile'))


@app.route('/updatePassword', methods=['POST'])
def updatePasswordSubmit():
  if not request.form['oldPsw'] == session['updatePassword']:
    alerte = "Le mot de passe temporaire est invalide. Veuillez recommencer."
  else:
    utilisateur = user.User.get_by_phone(session['phone'])
    utilisateur.password = request.form['password']
    utilisateur.update()
    session['password'] = utilisateur.password
    alerte = "Mise à jour pour l'identifiant " + session['phone']
  return redirect(url_for('updatePassword', alerte=alerte))


@app.route('/admin_readPosts')
def admin_readPosts():
  if session['phone'] == admin and session[
      'password'] == user.User.get_by_phone(admin).password:
    if post.Post.get_all() == []:
      return render_template(
        '404.html',
        message=Markup(
          "Aucune annonce pour l'instant :(<br>Revenez plus tard !"))
    else:
      adresse = []
      prixAsk = []
      prixPa = []
      description = []
      idUser = []
      idPost = []
      for i in post.Post.get_all():
        adresse.append(i.adresse)
        prixAsk.append(i.prixAsk)
        prixPa.append(i.prixPa)
        description.append(i.description)
        idUser.append(i.idUser)
        idPost.append(i.getId())
      rows = rows = zip(adresse, prixAsk, prixPa, description, idUser, idPost)
      return render_template('admin_readPosts.html', rows=rows)
  return redirect(url_for('profile'))


@app.route('/admin_readPosts/<idPostParameter>')
def admin_deletePost(idPostParameter):
  if session['phone'] == admin and session[
      'password'] == user.User.get_by_phone(admin).password:
    fav = favorites.Favorite.get_by_idPost(idPostParameter)
    for i in fav:
      i.delete()
    annonce = post.Post.get_by_id(idPostParameter)
    annonce.delete()
    return redirect(request.referrer)
  else:
    return redirect(url_for('profile'))


@app.route('/admin_updatePost', methods=['GET', 'POST'])
def admin_updatePostSubmit():
  annonce = post.Post.get_by_id(request.form['idPostParameter'])
  annonce.adresse = request.form['adresse']
  annonce.prixAsk = request.form['prixAsk']
  annonce.prixPa = request.form['prixPa']
  annonce.description = request.form['description']
  annonce.update()
  return redirect(url_for('admin_readPosts'))


if __name__ == '__main__':
  favorites.Favorite.init_database()
  # debug.Debug.deleteFavorites()
  # debug.Debug.deleteImages()
  # debug.Debug.deletePosts()
  # debug.Debug.isFavorite()
  # debug.Debug.isImage()
  # debug.Debug.isPost()
  post.Post.init_database()
  user.User.init_database()
  app.secret_key = 'super secret key'
  app.run(host='127.0.0.1', port=8080, debug=True)  #retrieve
#set FLASK_APP=main.py
#flask run
