// Importation des modules nécessaires depuis React et autres bibliothèques
import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode";
import { useHistory } from 'react-router-dom'; // Hook pour la gestion de l'historique de navigation

// Création du contexte d'authentification
const AuthContext = createContext();

export default AuthContext;

// Composant fournisseur de contexte d'authentification
export const AuthProvider = ({ children }) => {
 
  // Déclaration des états pour le jeton d'authentification et l'utilisateur
  // let [authToken, setAuthToken] = useState(null);
 // let [user, setUser] = useState(null);
  // let [authToken, setAuthToken] = useState(localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  let [authToken, setAuthToken] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  let [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null);
  let [loading, setLoading] = useState(true)
 
  
  // Hook pour accéder à l'historique de navigation
  const history = useHistory();

  // Fonction pour gérer la connexion de l'utilisateur
  let loginUser = async (e) => {
    e.preventDefault(); // Empêche le comportement par défaut du formulaire (rechargement de la page)

    // Envoi de la requête de connexion au serveur
    let response = await fetch('http://127.0.0.1:8000/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' // Indique que le corps de la requête est en JSON
      },
      body: JSON.stringify({ // Conversion des données du formulaire en JSON
        'username': e.target.username.value,
        'password': e.target.password.value
      })
    });
    
    // Extraction des données de la réponse en JSON
    let data = await response.json();
    
    // Vérification du statut de la réponse
    if (response.status === 200) {
      // Mise à jour des états avec les données de connexion
      setAuthToken(data);
      // Décodage du jeton d'accès pour obtenir les informations de l'utilisateur
      setUser(jwtDecode(data.access)); 
      
      // Stockage des jetons dans le localStorage pour persistance
      localStorage.setItem('authTokens', JSON.stringify(data));
      
      // Redirection vers la page d'accueil après la connexion
      history.push('/');
    } else {
      // Affichage d'un message d'erreur en cas de problème
      alert('Something went wrong');
    }
  };

// Fonction pour déconnecter l'utilisateur
let logoutUser = () => {
  // Supprime le jeton d'authentification (authToken)
  setAuthToken(null);

  // Supprime les informations de l'utilisateur (user)
  setUser(null);

  // Retire le jeton d'authentification stocké dans le localStorage
  localStorage.removeItem('authTokens');

  // Redirige l'utilisateur vers la page de connexion
  history.push('/login');
};

let updateToken = async () => {
  console.log('update token called!')
  let response = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json' // Indique que le corps de la requête est en JSON
    },
    body: JSON.stringify({'refresh':authToken.refresh})
  });
  let data = await response.json()
  if(response.status === 200){
      setAuthToken(data);
      setUser(jwtDecode(data.access)); 
      localStorage.setItem('authTokens', JSON.stringify(data));
  }else{
    logoutUser()
  }
}


  // Données du contexte fournies aux composants enfants
  let contextData = {
    user: user, // Informations de l'utilisateur
    loginUser: loginUser, // Fonction de connexion
    logoutUser:logoutUser, // Fonction de deconnexion
    authToken: authToken
  };
  useEffect(() =>{
    let fiveMinutes = 1000 * 60 *5
    let interval = setInterval(() =>{
       if(authToken){
         updateToken()
       }
     }, fiveMinutes)
     return () => clearInterval(interval)
   
   }, [authToken, loading])

  return (
    // Fourniture du contexte aux composants enfants
    <AuthContext.Provider value={contextData}>
      {children} 
    </AuthContext.Provider>
  );
};
