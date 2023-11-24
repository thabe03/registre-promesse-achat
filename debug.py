import favorites
import image
import user
import post
import os

class Debug:
  def allUsers():
    [print("tous les utilisateurs:"+str(i.getId())) for i in user.User.get_all()]
  
  def allPost_by_idUser(idUser):
    annonces = post.Post.get_by_idUser(idUser)
    [print("toutes les annonces pour cet utilisateur"+str(i.getId())) for i in annonces]
  
  def isPost():
    [print(i) for i in post.Post.get_all()]

  def isFavorite():
    [print(i.idPost,i.idUser,i.idUserOwner) for i in favorites.Favorite.get_all()] 
  
  def deletePosts():
    [i.delete() for i in post.Post.get_all()]

  def deleteFavorites():
    [i.delete() for i in favorites.Favorite.get_all()]