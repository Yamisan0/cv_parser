

import Link from 'next/link';


const HomePage = () => {
  return (
    <div>
      <h1>Bienvenue sur la page d'accueil</h1>
      <Link href="/login">Aller à la page de connexion</Link>
      <br />
      <Link href="/cv_test">Aller à la page de test de CV</Link>
    </div>
  );
};

export default HomePage;

