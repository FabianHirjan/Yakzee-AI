📖 Descriere
Yakzee-AI este un joc de zaruri unde utilizatorii pot rula zarurile, păstra anumite zaruri și alege combinații pentru a obține puncte. AI-ul numit "Bob" rulează zarurile automat și ia decizii pentru a-și maximiza scorul. Jocul se desfășoară pe 9 runde, iar câștigătorul este determinat pe baza scorului total acumulat.

💻 Cerințe de Sistem
Python 3.x
Pygame (pentru interfața grafică)
Sistem de operare compatibil cu Python (Windows, macOS, Linux)
🛠 Instalare
Clonează proiectul din GitHub:

bash
Copy code
git clone https://github.com/numele_tau/Yakzee-AI.git
cd Yakzee-AI
Creează și activează un mediu virtual (opțional, dar recomandat):

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate    # Windows
Instalează dependențele:

bash
Copy code
pip install -r requirements.txt
Rulează jocul:

bash
Copy code
python main.py
🎮 Cum se joacă
Jocul începe cu zarurile jucătorului afișate pe ecran.
Ai 3 rulări disponibile pentru a forma cea mai bună combinație de zaruri.
Apasă pe zarurile pe care dorești să le păstrezi și rulează restul pentru a găsi combinația ideală.
Alege o formație la sfârșitul rulărilor (sau o formație cu punctaj 0 dacă nu ai o combinație validă).
După turul jucătorului, AI-ul "Bob" își face tura automată.
Jocul se desfășoară pe 9 runde, iar la final, scorurile sunt afișate și câștigătorul este anunțat.
📝 Regulile Jocului
Small Straight: O secvență de 4 zaruri consecutive (ex: 1, 2, 3, 4).
Full House: Trei zaruri de un fel și două zaruri de alt fel.
Large Straight: O secvență de 5 zaruri consecutive.
Yahtzee: Cinci zaruri de același fel.
Chance: Puncte adunate din toate zarurile rulate.
🚀 Funcții Speciale
Adversar AI (Bob): Bob are propria strategie și tabele de scor. Rulările și deciziile sale sunt automate.
Afișare continuă a scorurilor: În timpul jocului, tabela de scor pentru jucător și Bob este afișată constant pe ecran.
Indicator pentru rulările rămase: În timpul fiecărei ture, poți vedea câte rulări îți mai rămân.
Anunțarea câștigătorului: La sfârșitul celor 9 runde, un label afișează câștigătorul.
