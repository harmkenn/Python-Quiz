import streamlit as st
import random

# --- Page Setup ---
if __name__ == "__main__":
    st.set_page_config(page_title="Italian Match", layout="wide")

# --- Load custom phrase set supplied by the user ---
ITALIAN_PHRASES = [
    # --- 1. BASIC GREETINGS & FORMALITIES ---
    ("Hi / Bye", "Ciao"),
    ("Good morning / Good day", "Buongiorno"),
    ("Good evening", "Buonasera"),
    ("Good night", "Buonanotte"),
    ("Hello (polite / neutral)", "Salve"),
    ("Goodbye", "Arrivederci"),
    ("See you soon", "A presto"),
    ("See you later", "A dopo"),
    ("See you", "Ci vediamo"),
    ("Please", "Per favore"),
    ("Thank you", "Grazie"),
    ("Thank you very much", "Grazie mille"),
    ("You're welcome", "Prego"),
    ("It's nothing / Don't mention it", "Di niente"),
    ("Excuse me (formal)", "Scusi"),
    ("Excuse me / Sorry", "Scusa"),
    ("Excuse me (to pass through)", "Permesso"),
    ("I'm sorry", "Mi dispiace"),
    ("Yes", "Sì"),
    ("No", "No"),
    ("All right / OK", "Va bene"),
    ("Pleased to meet you", "Piacere"),
    ("Welcome", "Benvenuto"),
    ("Have a good day", "Buona giornata"),
    ("Have a good evening", "Buona serata"),
    ("Have a good trip", "Buon viaggio"),
    ("Have a good weekend", "Buon fine settimana"),
    ("Have fun!", "Buon divertimento!"),
    ("Happy birthday!", "Buon compleanno!"),
    ("Congratulations!", "Congratulazioni!"),

    # --- 2. GETTING TO KNOW SOMEONE & SMALL TALK ---
    ("How are you? (formal)", "Come sta?"),
    ("How are you? (informal)", "Come stai?"),
    ("How's it going?", "Come va?"),
    ("I'm doing well, thank you", "Sto bene, grazie"),
    ("And you? (formal)", "E Lei?"),
    ("And you? (informal)", "E tu?"),
    ("What is your name? (informal)", "Come ti chiami?"),
    ("What is your name? (formal)", "Come si chiama?"),
    ("My name is...", "Mi chiamo..."),
    ("Where are you from? (informal)", "Di dove sei?"),
    ("Where are you from? (formal)", "Di dov'è?"),
    ("I am from...", "Sono di..."),
    ("How old are you?", "Quanti anni hai?"),
    ("I am ... years old", "Ho ... anni"),
    ("What do you do for a living?", "Cosa fai nella vita?"),
    ("What's up?", "Cosa si dice?"),
    ("Everything is good", "Tutto bene"),
    ("Not bad", "Non c'è male"),
    ("So-so", "Così così"),
    ("Where do you live?", "Dove abiti?"),
    ("I live in...", "Abito a..."),
    ("Are you here on vacation?", "Sei qui in vacanza?"),
    ("I am here for work", "Sono qui per lavoro"),
    ("Do you have family here?", "Hai famiglia qui?"),
    ("I am traveling alone", "Sto viaggiando da solo/a"),
    ("Who are you with?", "Con chi sei?"),
    ("I am here with my family", "Sono qui con la mia famiglia"),
    ("I am here with friends", "Sono qui con degli amici"),
    ("Nice to talk to you", "È stato un piacere parlare con te"),
    ("Let's keep in touch", "Teniamoci in contatto"),

    # --- 3. LANGUAGE & COMMUNICATION ---
    ("Do you speak English? (informal)", "Parli inglese?"),
    ("Do you speak English? (formal)", "Parla inglese?"),
    ("I speak a little Italian", "Parlo un po' di italiano"),
    ("I don't speak Italian", "Non parlo italiano"),
    ("I don't understand", "Non capisco"),
    ("I understand", "Capisco"),
    ("Can you speak more slowly?", "Può parlare più lentamente?"),
    ("Can you repeat that?", "Puoi ripetere?"),
    ("How do you say ... in Italian?", "Come si dice ... in italiano?"),
    ("What does that mean?", "Che cosa significa?"),
    ("Could you write it down, please?", "Può scriverlo, per favore?"),
    ("How do you spell it?", "Come si scrive?"),
    ("I am learning Italian", "Sto imparando l'italiano"),
    ("I got it / I understood", "Ho capito"),
    ("I didn't get it", "Non ho capito"),
    ("Can you help me? (formal)", "Può aiutarmi?"),
    ("Can you help me? (informal)", "Puoi aiutarmi?"),
    ("What did you say? (formal)", "Cosa ha detto?"),
    ("What did you say? (informal)", "Cosa hai detto?"),
    ("I have a question", "Ho una domanda"),
    ("No problem", "Nessun problema"),
    ("It doesn't matter / Never mind", "Non importa"),
    ("I don't know", "Non lo so"),
    ("I am sure of it", "Ne sono sicuro/a"),
    ("Are you sure?", "Sei sicuro/a?"),
    ("What is this called?", "Come si chiama questo?"),
    ("Could you speak a bit louder?", "Puoi parlare un po' più forte?"),
    ("My Italian is not very good", "Il mio italiano non è molto buono"),
    ("I understand a bit, but I can't speak well", "Capisco un po', ma non parlo bene"),
    ("Thanks for your patience", "Grazie per la pazienza"),

    # --- 4. NAVIGATION & DIRECTIONS ---
    ("Where is... ?", "Dov'è...?"),
    ("Where are...?", "Dove sono...?"),
    ("Where is the bathroom?", "Dov'è il bagno?"),
    ("Where is the station?", "Dov'è la stazione?"),
    ("Where is the bus stop?", "Dov'è la fermata dell'autobus?"),
    ("To the right", "A destra"),
    ("To the left", "A sinistra"),
    ("Straight ahead", "Dritto"),
    ("Straight on / Keep going straight", "Sempre dritto"),
    ("At the corner", "All'angolo"),
    ("Near", "Vicino"),
    ("Far", "Lontano"),
    ("Here", "Qui"),
    ("There", "Lì / Là"),
    ("Opposite / Facing", "Di fronte a"),
    ("Next to", "Accanto a"),
    ("How do I get to...?", "Come arrivo a...?"),
    ("Is it nearby?", "È vicino?"),
    ("Is it far from here?", "È lontano da qui?"),
    ("I am lost", "Mi sono perso / persa"),
    ("Where is the entrance?", "Dov'è l'ingresso?"),
    ("Where is the exit?", "Dov'è l'uscita?"),
    ("Cross the street", "Attraversa la strada"),
    ("Turn right at the traffic light", "Gira a destra al semaforo"),
    ("Take the first street on the left", "Prendi la prima strada a sinistra"),
    ("Behind the building", "Dietro l'edificio"),
    ("In front of the church", "Davanti alla chiesa"),
    ("Between the two shops", "Tra i due negozi"),
    ("How many minutes on foot?", "Quanti minuti a piedi?"),
    ("Is it safe to walk here?", "È sicuro camminare qui?"),

    # --- 5. TRAVEL, TRANSPORT & TICKETS ---
    ("Which platform?", "Quale binario?"),
    ("A ticket to..., please", "Un biglietto per..., per favore"),
    ("One way or round trip?", "Solo andata o ritorno?"),
    ("When does the train leave?", "Quando parte il treno?"),
    ("When does the bus arrive?", "Quando arriva l'autobus?"),
    ("Is this seat free?", "È libero questo posto?"),
    ("Where can I validate my ticket?", "Dove posso convalidare il biglietto?"),
    ("Is there a delay?", "C'è un ritardo?"),
    ("Which bus goes to the center?", "Quale autobus va in centro?"),
    ("Where do I get off?", "Dove devo scendere?"),
    ("I need a taxi", "Ho bisogno di un taxi"),
    ("Please take me to this address", "Mi porti a questo indirizzo, per favore"),
    ("How much to go to the airport?", "Quanto costa andare all'aeroporto?"),
    ("Stop here, please", "Si fermi qui, per favore"),
    ("Where is the baggage claim?", "Dov'è il ritiro bagagli?"),
    ("My luggage is lost", "Il mio bagaglio è smarrito"),
    ("I need to rent a car", "Devo noleggiare un'auto"),
    ("Where can I park?", "Dove posso parcheggiare?"),
    ("Is parking free?", "Il parcheggio è gratuito?"),
    ("Does this train stop in...?", "Questo treno ferma a...?"),

    # --- 6. DINING & DRINKING ---
    ("A table for two, please", "Un tavolo per due, per favore"),
    ("Can I see the menu?", "Posso vedere il menu?"),
    ("I would like to order", "Vorrei ordinare"),
    ("I would like...", "Vorrei..."),
    ("I'll have...", "Prendo..."),
    ("What do you recommend?", "Che cosa ci consiglia?"),
    ("What is the dish of the day?", "Qual è il piatto del giorno?"),
    ("An espresso, please", "Un caffè, per favore"),
    ("A cappuccino, please", "Un cappuccio, per favore"),
    ("A glass of water, please", "Un bicchiere d'acqua, per favore"),
    ("Still or sparkling water?", "Acqua naturale o frizzante?"),
    ("House wine", "Vino della casa"),
    ("A beer, please", "Una birra, per favore"),
    ("The bill, please", "Il conto, per favore"),
    ("Can I pay by card?", "Posso pagare con la carta?"),
    ("Do you accept credit cards?", "Accettate carte di credito?"),
    ("In cash", "In contanti"),
    ("It's my treat / I'm paying", "Offro io"),
    ("Keep the change", "Tenga il resto"),
    ("It’s delicious!", "È delizioso!"),
    ("It is very good", "È molto buono"),
    ("I am vegetarian", "Sono vegetariano/a"),
    ("I am vegan", "Sono vegano/a"),
    ("I am allergic to...", "Sono allergico/a a..."),
    ("Gluten-free", "Senza glutine"),
    ("Cheers!", "Salute!"),
    ("Enjoy your meal!", "Buon appetito!"),
    ("That's enough, thank you", "Basta così, grazie"),
    ("Where is the rest room?", "Dov'è la toilette?"),
    ("Can we have split bills?", "Possiamo avere due conti separati?"),
    ("A glass of red / white wine", "Un bicchiere di vino rosso / bianco"),
    ("Without ice, please", "Senza ghiaccio, per favore"),
    ("Could we have some bread?", "Possiamo avere del pane?"),
    ("Is service included?", "Il servizio è incluso?"),
    ("I didn't order this", "Non ho ordinato questo"),
    ("Is it spicy?", "È piccante?"),
    ("Another one, please", "Un altro, per favore"),
    ("Can I have a receipt?", "Posso avere la ricevuta?"),
    ("Is there a cover charge?", "C'è il coperto?"),
    ("To go / Takeaway", "Da asporto"),

    # --- 7. SHOPPING & MONEY ---
    ("How much does it cost?", "Quanto costa?"),
    ("How much do these cost?", "Quanto costano?"),
    ("It is too expensive", "È troppo caro"),
    ("Is there a discount?", "C'è uno sconto?"),
    ("I'm just looking, thank you", "Sto solo guardando, grazie"),
    ("Can I try it on?", "Posso provarlo?"),
    ("Where is the fitting room?", "Dov'è il camerino?"),
    ("Do you have a larger / smaller size?", "Ha una taglia più grande / piccola?"),
    ("I'll take it", "Lo prendo"),
    ("I don't want it", "Non lo voglio"),
    ("Do you have...?", "Avete...?"),
    ("What time do you close?", "A che ora chiudete?"),
    ("What time do you open?", "A che ora aprite?"),
    ("Is it open?", "È aperto?"),
    ("Is it closed?", "È chiuso?"),
    ("Where is the ATM?", "Dov'è il bancomat?"),
    ("Receipt, please", "Scontrino, per favore"),
    ("Can I have a bag?", "Posso avere un sacchetto?"),
    ("Do you have my size?", "Avete la mia taglia?"),
    ("What brand is it?", "Che marca è?"),
    ("Can we pay separately?", "Possiamo pagare separatamente?"),
    ("Do you have change?", "Avete il resto?"),
    ("Is it on sale?", "È in saldo?"),
    ("Where can I buy...?", "Dove posso comprare...?"),
    ("It's good quality", "È di buona qualità"),
    ("I'm looking for...", "Sto cercando..."),
    ("Can I pay with contactless?", "Posso pagare contactless?"),
    ("Do you have another color?", "Ne avete un altro colore?"),
    ("Can I exchange this?", "Posso cambiarlo?"),
    ("I'd like a refund", "Vorrei un rimborso"),

    # --- 8. ACCOMMODATIONS & HOTELS ---
    ("I have a reservation", "Ho una prenotazione"),
    ("Under the name...", "A nome di..."),
    ("Do you have a vacant room?", "Avete una camera libera?"),
    ("For how many nights?", "Per quante notti?"),
    ("For one night / two nights", "Per una notte / due notti"),
    ("Single / Double room", "Camera singola / doppia"),
    ("With a double bed", "Con letto matrimoniale"),
    ("Is breakfast included?", "La colazione è inclusa?"),
    ("What time is check-out?", "A che ora è il check-out?"),
    ("Can I leave my luggage here?", "Posso lasciare i bagagli qui?"),
    ("The key, please", "La chiave, per favore"),
    ("The air conditioning doesn't work", "L'aria condizionata non funziona"),
    ("There is no hot water", "Non c'è acqua calda"),
    ("What is the Wi-Fi password?", "Qual è la password del Wi-Fi?"),
    ("Could I have an extra towel?", "Posso avere un asciugamano in più?"),
    ("Where is the elevator?", "Dov'è l'ascensore?"),
    ("It's very noisy", "È molto rumoroso"),
    ("Can you wake me up at 7?", "Può svegliarmi alle sette?"),
    ("Is there a safe in the room?", "C'è una cassaforte in camera?"),
    ("I had a great stay", "Mi sono trovato/a benissimo"),

    # --- 9. TIME, DATES & WEATHER ---
    ("What time is it?", "Che ora è?"),
    ("It is one o'clock", "È l'una"),
    ("It is two / three / four o'clock", "Sono le due / tre / quattro"),
    ("Today", "Oggi"),
    ("Tomorrow", "Domani"),
    ("Yesterday", "Ieri"),
    ("Tonight / This evening", "Stasera"),
    ("This morning", "Stamattina"),
    ("Afternoon", "Pomeriggio"),
    ("Now", "Adesso"),
    ("Later", "Più tardi"),
    ("Before", "Prima"),
    ("After", "Dopo"),
    ("Early / Soon", "Presto"),
    ("Late", "Tardi"),
    ("The weekend", "Il fine settimana"),
    ("What day is today?", "Che giorno è oggi?"),
    ("At what time?", "A che ora?"),
    ("In a short while", "Tra poco"),
    ("Always / Never", "Sempre / Mai"),
    ("See you tomorrow", "A domani"),
    ("Yesterday evening", "Ieri sera"),
    ("Next week", "La settimana prossima"),
    ("Last week", "La settimana scorsa"),
    ("What's the weather like?", "Che tempo fa?"),
    ("It's nice weather", "Fa bel tempo"),
    ("It's cold / hot", "Fa freddo / caldo"),
    ("It's raining", "Sta piovendo"),
    ("It's sunny", "C'è il sole"),
    ("It's windy", "C'è vento"),

    # --- 10. EMERGENCIES, MEDICAL & SAFETY ---
    ("Help!", "Aiuto!"),
    ("Call the police!", "Chiami la polizia!"),
    ("Call an ambulance!", "Chiami un'ambulanza!"),
    ("I need a doctor", "Ho bisogno di un medico"),
    ("Where is the hospital?", "Dov'è l'ospedale?"),
    ("Where is the pharmacy?", "Dov'è la farmacia?"),
    ("I feel sick", "Mi sento male"),
    ("I have pain here", "Ho dolore qui"),
    ("Watch out! / Be careful!", "Attento! / Attenta!"),
    ("I lost my passport", "Ho perso il mio passaporto"),
    ("I lost my phone", "Ho perso il telefono"),
    ("There has been an accident", "C'è stato un incidente"),
    ("Emergency", "Emergenza"),
    ("I am unwell", "Sto male"),
    ("Go away!", "Vai via!"),
    ("I was robbed", "Sono stato/a derubato/a"),
    ("Where is the police station?", "Dov'è la questura?"),
    ("I have a fever", "Ho la febbre"),
    ("I need medicine for...", "Ho bisogno di una medicina per..."),
    ("I am allergic to penicillin", "Sono allergico/a alla penicillina"),
    ("My head hurts", "Mi fa male la testa"),
    ("My stomach hurts", "Mi fa male lo stomaco"),
    ("Call a doctor, please", "Chiami un medico, per favore"),
    ("Stop, thief!", "Al ladro!"),
    ("I lost my wallet", "Ho perso il portafoglio"),

    # --- 11. TECHNOLOGY & PHONES ---
    ("Is there Wi-Fi here?", "C'è il Wi-Fi qui?"),
    ("Can I charge my phone here?", "Posso caricare il telefono qui?"),
    ("Do you have a phone charger?", "Hai un caricabatterie?"),
    ("Where can I buy a SIM card?", "Dove posso comprare una SIM?"),
    ("There is no signal", "Non c'è campo"),
    ("My phone is dead", "Il mio telefono è scarico"),
    ("What is the phone number?", "Qual è il numero di telefono?"),
    ("Can I take a picture?", "Posso fare una foto?"),
    ("Would you take a picture of us?", "Ci fa una foto, per favore?"),
    ("Send me a message", "Mandami un messaggio"),

    # --- 12. EXPRESSING OPINIONS, FEELINGS & NEEDS ---
    ("I like it", "Mi piace"),
    ("I don't like it", "Non mi piace"),
    ("I love it!", "Lo adoro! / Mi piace tantissimo!"),
    ("I agree", "Sono d'accordo"),
    ("I disagree", "Non sono d'accordo"),
    ("I think that...", "Penso che..."),
    ("In my opinion", "Secondo me"),
    ("I need...", "Ho bisogno di..."),
    ("I want...", "Voglio..."),
    ("I don't care", "Non me ne importa"),
    ("I'm tired", "Sono stanco/a"),
    ("I'm hungry", "Ho fame"),
    ("I'm thirsty", "Ho sete"),
    ("I'm cold / hot", "Ho freddo / caldo"),
    ("I'm sleepy", "Ho sonno"),
    ("I'm busy", "Sono occupato/a"),
    ("I'm ready", "Sono pronto/a"),
    ("I am happy", "Sono contento/a"),
    ("I am sad", "Sono triste"),
    ("Don't worry", "Non ti preoccupare / Non si preoccupi"),

    # --- 13. IDIOMS, SLANG & EXPRESSIONS ---
    ("How wonderful!", "Che bello!"),
    ("What a pity! / What a shame!", "Che peccato!"),
    ("Oh my goodness!", "Mamma mia!"),
    ("Good luck!", "In bocca al lupo!"),
    ("Response to 'In bocca al lupo'", "Crepi il lupo!"),
    ("Makes sense / Sounds good", "Ci sta"),
    ("Thank goodness!", "Meno male!"),
    ("I wish! / If only!", "Magari!"),
    ("Come on! / Stop it!", "Dai!"),
    ("I don't know / Beats me!", "Boh!"),
    ("I can't wait", "Non vedo l'ora"),
    ("To be in a bad mood", "Avere la luna storta"),
    ("To kill two birds with one stone", "Prendere due piccioni con una fava"),
    ("The sweetness of doing nothing", "La dolce far niente"),
    ("What a mess!", "Che casino!"),
    ("Are you kidding?", "Ma stai scherzando?"),
    ("Whatever! / Forget it!", "Lascia perdere!"),
    ("Exactly!", "Esatto!"),
    ("Fingers crossed!", "Incrociamo le dita!"),
    ("To cost an arm and a leg", "Costare un occhio della testa"),
    ("To hit the nail on the head", "Colpire nel segno"),
    ("It's not a big deal", "Non è la fine del mondo"),
    ("Out of the blue", "All'improvviso"),
    ("Speak of the devil", "Parli del diavolo e spuntano le corna"),
    ("I'm exhausted / dead tired", "Sono distrutto/a")
]

italian_set = dict(ITALIAN_PHRASES)

def app():
    st.markdown("""
    <style>
    .big-font { font-size: 20px !important; text-align: center; }
    .stButton button { height: 60px; width: 100%; font-size: 16px; white-space: normal; word-wrap: break-word; padding: 0.25rem 0.5rem !important; }
    .team-current { font-weight: 700; color: green; }
    .score-label { font-size: 24px; font-weight: bold; text-align: center; }
    .row-space { margin-top: 8px; }
    .card-selected { border: 3px solid yellow !important; }
    .card-matched { opacity: 0.5; }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar: Game Setup ---
    st.sidebar.header("🎮 Game Setup")
    num_pairs = st.sidebar.slider("Number of word pairs:", 10, len(italian_set), 20, step=1)
    num_teams = st.sidebar.slider("Number of teams:", 2, 4, 4, step=1)

    # --- Initialize game ---
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
        st.session_state.num_teams = num_teams
    
    # Use stored num_teams if game is already running, otherwise use slider value
    if st.session_state.initialized:
        num_teams = st.session_state.num_teams
    
    team_colors = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"][:num_teams]

    if st.sidebar.button("🔁 Start New Game") or not st.session_state.initialized:
        st.session_state.num_teams = num_teams
        selected = random.sample(list(italian_set.items()), num_pairs)
        pairs = []
        for eng, ita in selected:
            pairs.append((eng, "eng"))
            pairs.append((ita, "ita"))
        random.shuffle(pairs)

        st.session_state.cards = pairs
        st.session_state.selected = []
        st.session_state.matched = []
        st.session_state.matched_by_team = {}
        st.session_state.matched_history = []  # <--- Stores ordered tuples: (english, italian, team_idx)
        st.session_state.turns = 0
        st.session_state.team_scores = [0] * num_teams
        st.session_state.current_team = random.randint(0, num_teams - 1)
        st.session_state.initialized = True
        st.rerun()

    # --- Matching logic ---
    def is_matching_pair(idx1, idx2):
        card1, type1 = st.session_state.cards[idx1]
        card2, type2 = st.session_state.cards[idx2]
        if type1 == type2:
            return False
        if type1 == "eng":
            return italian_set[card1] == card2
        else:
            return italian_set[card2] == card1

    def flip_card(index):
        if index in st.session_state.matched or index in st.session_state.selected:
            return

        st.session_state.selected.append(index)

        if len(st.session_state.selected) == 2:
            idx1, idx2 = st.session_state.selected
            st.session_state.turns += 1
            if is_matching_pair(idx1, idx2):
                st.session_state.matched.extend([idx1, idx2])
                team = st.session_state.current_team
                st.session_state.matched_by_team[idx1] = team
                st.session_state.matched_by_team[idx2] = team
                st.session_state.team_scores[team] += 1
                
                # Retrieve normalized english and italian phrases for history logging
                c1_text, c1_type = st.session_state.cards[idx1]
                c2_text, c2_type = st.session_state.cards[idx2]
                eng_phrase = c1_text if c1_type == "eng" else c2_text
                ita_phrase = c2_text if c1_type == "eng" else c1_text
                
                # Append to match history
                st.session_state.matched_history.append((eng_phrase, ita_phrase, team))
                
                st.session_state.selected = []
            else:
                st.session_state.selected = []
                st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)

    # --- Team controls ---
    if st.sidebar.button("🔀 Switch Team"):
        st.session_state.selected = []
        st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)

    # --- Display Board ---
    st.markdown(f"### Current turn: Team {st.session_state.current_team + 1}")
    cols_per_row = 6
    num_cards = len(st.session_state.cards)

    for start in range(0, num_cards, cols_per_row):
        cols = st.columns(cols_per_row)
        for i, col in enumerate(cols):
            idx = start + i
            if idx >= num_cards:
                continue
            card, ctype = st.session_state.cards[idx]
            with col:
                if idx in st.session_state.matched:
                    team = st.session_state.matched_by_team.get(idx, 0)
                    color = team_colors[team]
                    st.markdown(f"<div class='big-font card-matched' style='color:{color}'>{card}</div>", unsafe_allow_html=True)
                else:
                    is_selected = idx in st.session_state.selected
                    button_style = " card-selected" if is_selected else ""
                    if st.button(f"{card}", key=f"card-{idx}"):
                        flip_card(idx)
        st.markdown("<div class='row-space'></div>", unsafe_allow_html=True)

    # --- Scores ---
    st.markdown("---")
    score_cols = st.columns(len(st.session_state.team_scores))
    for t in range(len(st.session_state.team_scores)):
        color = team_colors[t]
        label = f"Team {t+1}: {st.session_state.team_scores[t]}"
        if t == st.session_state.current_team:
            score_cols[t].markdown(f"<div class='score-label team-current' style='color:{color}'>{label} ⬅️</div>", unsafe_allow_html=True)
        else:
            score_cols[t].markdown(f"<div class='score-label' style='color:{color}'>{label}</div>", unsafe_allow_html=True)

    st.markdown(f"**Turns taken:** {st.session_state.turns}")

    # --- Live Matched Pairs List ---
    st.markdown("---")
    st.subheader("📝 Matched Pairs History (In Order)")
    
    if len(st.session_state.matched_history) == 0:
        st.caption("No pairs matched yet. Flip cards to make a match!")
    else:
        for idx, (eng, ita, team_idx) in enumerate(st.session_state.matched_history, 1):
            t_color = team_colors[team_idx]
            st.markdown(
                f"**{idx}.** {eng} ↔️ **{ita}** "
                f"<span style='color:{t_color}; font-weight:bold;'>(Matched by Team {team_idx + 1})</span>",
                unsafe_allow_html=True
            )

    # --- Game Over ---
    if len(st.session_state.matched) == len(st.session_state.cards):
        st.success("🎉 Game Over! All pairs matched!")
        winner = max(range(len(st.session_state.team_scores)), key=lambda i: st.session_state.team_scores[i])
        st.info(f"🏆 Winner: Team {winner + 1} with {st.session_state.team_scores[winner]} points!")

    # --- Restart ---
    if st.button("🔁 Restart Game"):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    app()
