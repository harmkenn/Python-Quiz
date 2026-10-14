import streamlit as st
import random

# --- Page Setup ---
if __name__ == "__main__":
    st.set_page_config(page_title="Italian Match", layout="wide")

# --- Load custom phrase set with Word-for-Word literal translations ---
ITALIAN_PHRASES = [
    # --- 1. BASIC GREETINGS & FORMALITIES ---
    ("Hi / Bye", "Ciao"),
    ("Good morning / Good day [Lit: Good day]", "Buongiorno"),
    ("Good evening [Lit: Good evening]", "Buonasera"),
    ("Good night [Lit: Good night]", "Buonanotte"),
    ("Hello (polite / neutral) [Lit: Safe/Healthy]", "Salve"),
    ("Goodbye [Lit: Until seeing each other again]", "Arrivederci"),
    ("See you soon [Lit: To soon]", "A presto"),
    ("See you later [Lit: To after]", "A dopo"),
    ("See you [Lit: Us we see]", "Ci vediamo"),
    ("Please [Lit: For favor]", "Per favore"),
    ("Thank you [Lit: Graces/Thanks]", "Grazie"),
    ("Thank you very much [Lit: Thousand thanks]", "Grazie mille"),
    ("You're welcome [Lit: I pray/ask]", "Prego"),
    ("It's nothing / Don't mention it [Lit: Of nothing]", "Di niente"),
    ("Excuse me (formal) [Lit: Excuse (you)]", "Scusi"),
    ("Excuse me / Sorry [Lit: Excuse (thou)]", "Scusa"),
    ("Excuse me (to pass through) [Lit: Permission]", "Permesso"),
    ("I'm sorry [Lit: To me it displeases]", "Mi dispiace"),
    ("Yes", "Sì"),
    ("No", "No"),
    ("All right / OK [Lit: It goes well]", "Va bene"),
    ("Pleased to meet you [Lit: Pleasure]", "Piacere"),
    ("Welcome [Lit: Well come]", "Benvenuto"),
    ("Have a good day [Lit: Good day-duration]", "Buona giornata"),
    ("Have a good evening [Lit: Good evening-duration]", "Buona serata"),
    ("Have a good trip [Lit: Good voyage]", "Buon viaggio"),
    ("Have a good weekend [Lit: Good end week]", "Buon fine settimana"),
    ("Have fun! [Lit: Good fun!]", "Buon divertimento!"),
    ("Happy birthday! [Lit: Good birthday!]", "Buon compleanno!"),
    ("Congratulations! [Lit: Congratulations!]", "Congratulazioni!"),

    # --- 2. GETTING TO KNOW SOMEONE & SMALL TALK ---
    ("How are you? (formal) [Lit: How stay (you)]", "Come sta?"),
    ("How are you? (informal) [Lit: How stay (thou)]", "Come stai?"),
    ("How's it going? [Lit: How goes?]", "Come va?"),
    ("I'm doing well, thank you [Lit: I stay well, thanks]", "Sto bene, grazie"),
    ("And you? (formal) [Lit: And You?]", "E Lei?"),
    ("And you? (informal) [Lit: And thou?]", "E tu?"),
    ("What is your name? (informal) [Lit: How yourself call-you?]", "Come ti chiami?"),
    ("What is your name? (formal) [Lit: How yourself call-You?]", "Come si chiama?"),
    ("My name is... [Lit: Myself I call...]", "Mi chiamo..."),
    ("Where are you from? (informal) [Lit: Of where art-thou?]", "Di dove sei?"),
    ("Where are you from? (formal) [Lit: Of where is-You?]", "Di dov'è?"),
    ("I am from... [Lit: I am of...]", "Sono di..."),
    ("How old are you? [Lit: How many years have-thou?]", "Quanti anni hai?"),
    ("I am ... years old [Lit: I have ... years]", "Ho ... anni"),
    ("What do you do for a living? [Lit: What do-thou in the life?]", "Cosa fai nella vita?"),
    ("What's up? [Lit: What self says?]", "Cosa si dice?"),
    ("Everything is good [Lit: All well]", "Tutto bene"),
    ("Not bad [Lit: Not there is bad]", "Non c'è male"),
    ("So-so [Lit: Like this like this]", "Così così"),
    ("Where do you live? [Lit: Where live-thou?]", "Dove abiti?"),
    ("I live in... [Lit: I live at...]", "Abito a..."),
    ("Are you here on vacation? [Lit: Art-thou here in vacation?]", "Sei qui in vacanza?"),
    ("I am here for work [Lit: I am here for work]", "Sono qui per lavoro"),
    ("Do you have family here? [Lit: Hast-thou family here?]", "Hai famiglia qui?"),
    ("I am traveling alone [Lit: I stay traveling from alone]", "Sto viaggiando da solo/a"),
    ("Who are you with? [Lit: With whom art-thou?]", "Con chi sei?"),
    ("I am here with my family [Lit: I am here with the my family]", "Sono qui con la mia famiglia"),
    ("I am here with friends [Lit: I am here with of the friends]", "Sono qui con degli amici"),
    ("Nice to talk to you [Lit: It was a pleasure to talk with thee]", "È stato un piacere parlare con te"),
    ("Let's keep in touch [Lit: Hold ourselves in contact]", "Teniamoci in contatto"),

    # --- 3. LANGUAGE & COMMUNICATION ---
    ("Do you speak English? (informal) [Lit: Speak-thou English?]", "Parli inglese?"),
    ("Do you speak English? (formal) [Lit: Speaks-You English?]", "Parla inglese?"),
    ("I speak a little Italian [Lit: I speak a little of Italian]", "Parlo un po' di italiano"),
    ("I don't speak Italian [Lit: Not I speak Italian]", "Non parlo italiano"),
    ("I don't understand [Lit: Not I understand]", "Non capisco"),
    ("I understand [Lit: I understand]", "Capisco"),
    ("Can you speak more slowly? [Lit: Can-You speak more slowly?]", "Può parlare più lentamente?"),
    ("Can you repeat that? [Lit: Can-thou repeat?]", "Puoi ripetere?"),
    ("How do you say ... in Italian? [Lit: How self says ... in Italian?]", "Come si dice ... in italiano?"),
    ("What does that mean? [Lit: What thing signifies?]", "Che cosa significa?"),
    ("Could you write it down, please? [Lit: Can-You write it, for favor?]", "Può scriverlo, per favore?"),
    ("How do you spell it? [Lit: How self writes?]", "Come si scrive?"),
    ("I am learning Italian [Lit: I stay learning the Italian]", "Sto imparando l'italiano"),
    ("I got it / I understood [Lit: I have understood]", "Ho capito"),
    ("I didn't get it [Lit: Not I have understood]", "Non ho capito"),
    ("Can you help me? (formal) [Lit: Can-You help me?]", "Può aiutarmi?"),
    ("Can you help me? (informal) [Lit: Can-thou help me?]", "Puoi aiutarmi?"),
    ("What did you say? (formal) [Lit: What has-You said?]", "Cosa ha detto?"),
    ("What did you say? (informal) [Lit: What hast-thou said?]", "Cosa hai detto?"),
    ("I have a question [Lit: I have a question]", "Ho una domanda"),
    ("No problem [Lit: No problem]", "Nessun problema"),
    ("It doesn't matter / Never mind [Lit: Not imports]", "Non importa"),
    ("I don't know [Lit: Not it I know]", "Non lo so"),
    ("I am sure of it [Lit: Of it I am sure]", "Ne sono sicuro/a"),
    ("Are you sure? [Lit: Art-thou sure?]", "Sei sicuro/a?"),
    ("What is this called? [Lit: How self calls this?]", "Come si chiama questo?"),
    ("Could you speak a bit louder? [Lit: Can-thou speak a bit more strong?]", "Puoi parlare un po' più forte?"),
    ("My Italian is not very good [Lit: The my Italian not is very good]", "Il mio italiano non è molto buono"),
    ("I understand a bit, but I can't speak well [Lit: I understand a bit, but not I speak well]", "Capisco un po', ma non parlo bene"),
    ("Thanks for your patience [Lit: Thanks for the patience]", "Grazie per la pazienza"),

    # --- 4. NAVIGATION & DIRECTIONS ---
    ("Where is... ? [Lit: Where is...?]", "Dov'è...?"),
    ("Where are...? [Lit: Where are...?]", "Dove sono...?"),
    ("Where is the bathroom? [Lit: Where is the bath?]", "Dov'è il bagno?"),
    ("Where is the station? [Lit: Where is the station?]", "Dov'è la stazione?"),
    ("Where is the bus stop? [Lit: Where is the stop of the bus?]", "Dov'è la fermata dell'autobus?"),
    ("To the right [Lit: At right]", "A destra"),
    ("To the left [Lit: At left]", "A sinistra"),
    ("Straight ahead [Lit: Straight]", "Dritto"),
    ("Straight on / Keep going straight [Lit: Always straight]", "Sempre dritto"),
    ("At the corner [Lit: At the corner]", "All'angolo"),
    ("Near [Lit: Near]", "Vicino"),
    ("Far [Lit: Far]", "Lontano"),
    ("Here [Lit: Here]", "Qui"),
    ("There [Lit: There / There]", "Lì / Là"),
    ("Opposite / Facing [Lit: Of front to]", "Di fronte a"),
    ("Next to [Lit: Alongside to]", "Accanto a"),
    ("How do I get to...? [Lit: How arrive-I to...?]", "Come arrivo a...?"),
    ("Is it nearby? [Lit: Is near?]", "È vicino?"),
    ("Is it far from here? [Lit: Is far from here?]", "È lontano da qui?"),
    ("I am lost [Lit: Myself I am lost]", "Mi sono perso / persa"),
    ("Where is the entrance? [Lit: Where is the entry?]", "Dov'è l'ingresso?"),
    ("Where is the exit? [Lit: Where is the exit?]", "Dov'è l'uscita?"),
    ("Cross the street [Lit: Cross the street]", "Attraversa la strada"),
    ("Turn right at the traffic light [Lit: Turn at right at the traffic-light]", "Gira a destra al semaforo"),
    ("Take the first street on the left [Lit: Take the first street at left]", "Prendi la prima strada a sinistra"),
    ("Behind the building [Lit: Behind the building]", "Dietro l'edificio"),
    ("In front of the church [Lit: Before at the church]", "Davanti alla chiesa"),
    ("Between the two shops [Lit: Between the two shops]", "Tra i due negozi"),
    ("How many minutes on foot? [Lit: How many minutes at feet?]", "Quanti minuti a piedi?"),
    ("Is it safe to walk here? [Lit: Is safe to walk here?]", "È sicuro camminare qui?"),

    # --- 5. TRAVEL, TRANSPORT & TICKETS ---
    ("Which platform? [Lit: Which track?]", "Quale binario?"),
    ("A ticket to..., please [Lit: A ticket for..., for favor]", "Un biglietto per..., per favore"),
    ("One way or round trip? [Lit: Only going or return?]", "Solo andata o ritorno?"),
    ("When does the train leave? [Lit: When departs the train?]", "Quando parte il treno?"),
    ("When does the bus arrive? [Lit: When arrives the bus?]", "Quando arriva l'autobus?"),
    ("Is this seat free? [Lit: Is free this seat?]", "È libero questo posto?"),
    ("Where can I validate my ticket? [Lit: Where can-I to-validate the ticket?]", "Dove posso convalidare il biglietto?"),
    ("Is there a delay? [Lit: There is a delay?]", "C'è un ritardo?"),
    ("Which bus goes to the center? [Lit: Which bus goes in center?]", "Quale autobus va in centro?"),
    ("Where do I get off? [Lit: Where must-I to-descend?]", "Dove devo scendere?"),
    ("I need a taxi [Lit: I have need of a taxi]", "Ho bisogno di un taxi"),
    ("Please take me to this address [Lit: Me carry-You to this address, for favor]", "Mi porti a questo indirizzo, per favore"),
    ("How much to go to the airport? [Lit: How much costs to go to the airport?]", "Quanto costa andare all'aeroporto?"),
    ("Stop here, please [Lit: Yourself stop-You here, for favor]", "Si fermi qui, per favore"),
    ("Where is the baggage claim? [Lit: Where is the withdrawal bags?]", "Dov'è il ritiro bagagli?"),
    ("My luggage is lost [Lit: The my baggage is lost]", "Il mio bagaglio è smarrito"),
    ("I need to rent a car [Lit: Must-I to-rent a car]", "Devo noleggiare un'auto"),
    ("Where can I park? [Lit: Where can-I to-park?]", "Dove posso parcheggiare?"),
    ("Is parking free? [Lit: The parking is free?]", "Il parcheggio è gratuito?"),
    ("Does this train stop in...? [Lit: This train stops in...?]", "Questo treno ferma a...?"),

    # --- 6. DINING & DRINKING ---
    ("A table for two, please [Lit: A table for two, for favor]", "Un tavolo per due, per favore"),
    ("Can I see the menu? [Lit: Can-I to-see the menu?]", "Posso vedere il menu?"),
    ("I would like to order [Lit: I would wish to order]", "Vorrei ordinare"),
    ("I would like... [Lit: I would wish...]", "Vorrei..."),
    ("I'll have... [Lit: I take...]", "Prendo..."),
    ("What do you recommend? [Lit: What thing to us recommend-You?]", "Che cosa ci consiglia?"),
    ("What is the dish of the day? [Lit: Which is the dish of the day?]", "Qual è il piatto del giorno?"),
    ("An espresso, please [Lit: A coffee, for favor]", "Un caffè, per favore"),
    ("A cappuccino, please [Lit: A cappuccino, for favor]", "Un cappuccio, per favore"),
    ("A glass of water, please [Lit: A glass of water, for favor]", "Un bicchiere d'acqua, per favore"),
    ("Still or sparkling water? [Lit: Water natural or sparkling?]", "Acqua naturale o frizzante?"),
    ("House wine [Lit: Wine of the house]", "Vino della casa"),
    ("A beer, please [Lit: A beer, for favor]", "Una birra, per favore"),
    ("The bill, please [Lit: The account, for favor]", "Il conto, per favore"),
    ("Can I pay by card? [Lit: Can-I to-pay with the card?]", "Posso pagare con la carta?"),
    ("Do you accept credit cards? [Lit: Accept-you cards of credit?]", "Accettate carte di credito?"),
    ("In cash [Lit: In cash-money]", "In contanti"),
    ("It's my treat / I'm paying [Lit: Offer I]", "Offro io"),
    ("Keep the change [Lit: Keep-You the remainder]", "Tenga il resto"),
    ("It’s delicious! [Lit: It is delicious!]", "È delizioso!"),
    ("It is very good [Lit: It is very good]", "È molto buono"),
    ("I am vegetarian [Lit: I am vegetarian]", "Sono vegetariano/a"),
    ("I am vegan [Lit: I am vegan]", "Sono vegano/a"),
    ("I am allergic to... [Lit: I am allergic to...]", "Sono allergico/a a..."),
    ("Gluten-free [Lit: Without gluten]", "Senza glutine"),
    ("Cheers! [Lit: Health!]", "Salute!"),
    ("Enjoy your meal! [Lit: Good appetite!]", "Buon appetito!"),
    ("That's enough, thank you [Lit: Enough like this, thanks]", "Basta così, grazie"),
    ("Where is the rest room? [Lit: Where is the toilet?]", "Dov'è la toilette?"),
    ("Can we have split bills? [Lit: Can-we to-have two accounts separated?]", "Possiamo avere due conti separati?"),
    ("A glass of red / white wine [Lit: A glass of wine red / white]", "Un bicchiere di vino rosso / bianco"),
    ("Without ice, please [Lit: Without ice, for favor]", "Senza ghiaccio, per favore"),
    ("Could we have some bread? [Lit: Can-we to-have of the bread?]", "Possiamo avere del pane?"),
    ("Is service included? [Lit: The service is included?]", "Il servizio è incluso?"),
    ("I didn't order this [Lit: Not I have ordered this]", "Non ho ordinato questo"),
    ("Is it spicy? [Lit: Is spicy?]", "È piccante?"),
    ("Another one, please [Lit: An other, for favor]", "Un altro, per favore"),
    ("Can I have a receipt? [Lit: Can-I to-have the receipt?]", "Posso avere la ricevuta?"),
    ("Is there a cover charge? [Lit: There is the cover-charge?]", "C'è il coperto?"),
    ("To go / Takeaway [Lit: From transport]", "Da asporto"),

    # --- 7. SHOPPING & MONEY ---
    ("How much does it cost? [Lit: How much costs?]", "Quanto costa?"),
    ("How much do these cost? [Lit: How much cost-they?]", "Quanto costano?"),
    ("It is too expensive [Lit: It is too dear]", "È troppo caro"),
    ("Is there a discount? [Lit: There is a discount?]", "C'è uno sconto?"),
    ("I'm just looking, thank you [Lit: I stay only looking, thanks]", "Sto solo guardando, grazie"),
    ("Can I try it on? [Lit: Can-I to-try-it?]", "Posso provarlo?"),
    ("Where is the fitting room? [Lit: Where is the dressing-room?]", "Dov'è il camerino?"),
    ("Do you have a larger / smaller size? [Lit: Have-You a size more big / small?]", "Ha una taglia più grande / piccola?"),
    ("I'll take it [Lit: It I take]", "Lo prendo"),
    ("I don't want it [Lit: Not it I want]", "Non lo voglio"),
    ("Do you have...? [Lit: Have-you...?]", "Avete...?"),
    ("What time do you close? [Lit: At what hour close-you?]", "A che ora chiudete?"),
    ("What time do you open? [Lit: At what hour open-you?]", "A che ora aprite?"),
    ("Is it open? [Lit: Is open?]", "È aperto?"),
    ("Is it closed? [Lit: Is closed?]", "È chiuso?"),
    ("Where is the ATM? [Lit: Where is the bank-machine?]", "Dov'è il bancomat?"),
    ("Receipt, please [Lit: Receipt, for favor]", "Scontrino, per favore"),
    ("Can I have a bag? [Lit: Can-I to-have a bag?]", "Posso avere un sacchetto?"),
    ("Do you have my size? [Lit: Have-you the my size?]", "Avete la mia taglia?"),
    ("What brand is it? [Lit: What brand is?]", "Che marca è?"),
    ("Can we pay separately? [Lit: Can-we to-pay separately?]", "Possiamo pagare separatamente?"),
    ("Do you have change? [Lit: Have-you the remainder?]", "Avete il resto?"),
    ("Is it on sale? [Lit: Is in sale/discount?]", "È in saldo?"),
    ("Where can I buy...? [Lit: Where can-I to-buy...?]", "Dove posso comprare...?"),
    ("It's good quality [Lit: It is of good quality]", "È di buona qualità"),
    ("I'm looking for... [Lit: I stay searching...]", "Sto cercando..."),
    ("Can I pay with contactless? [Lit: Can-I to-pay contactless?]", "Posso pagare contactless?"),
    ("Do you have another color? [Lit: Of it have-you an other color?]", "Ne avete un altro colore?"),
    ("Can I exchange this? [Lit: Can-I to-change-it?]", "Posso cambiarlo?"),
    ("I'd like a refund [Lit: I would wish a refund]", "Vorrei un rimborso"),

    # --- 8. ACCOMMODATIONS & HOTELS ---
    ("I have a reservation [Lit: I have a reservation]", "Ho una prenotazione"),
    ("Under the name... [Lit: At name of...]", "A nome di..."),
    ("Do you have a vacant room? [Lit: Have-you a room free?]", "Avete una camera libera?"),
    ("For how many nights? [Lit: For how-many nights?]", "Per quante notti?"),
    ("For one night / two nights [Lit: For one night / two nights]", "Per una notte / due notti"),
    ("Single / Double room [Lit: Room single / double]", "Camera singola / doppia"),
    ("With a double bed [Lit: With bed matrimonial]", "Con letto matrimoniale"),
    ("Is breakfast included? [Lit: The breakfast is included?]", "La colazione è inclusa?"),
    ("What time is check-out? [Lit: At what hour is the check-out?]", "A che ora è il check-out?"),
    ("Can I leave my luggage here? [Lit: Can-I to-leave the baggages here?]", "Posso lasciare i bagagli qui?"),
    ("The key, please [Lit: The key, for favor]", "La chiave, per favore"),
    ("The air conditioning doesn't work [Lit: The air conditioned not works]", "L'aria condizionata non funziona"),
    ("There is no hot water [Lit: Not there is water hot]", "Non c'è acqua calda"),
    ("What is the Wi-Fi password? [Lit: Which is the password of the Wi-Fi?]", "Qual è la password del Wi-Fi?"),
    ("Could I have an extra towel? [Lit: Can-I to-have a towel in more?]", "Posso avere un asciugamano in più?"),
    ("Where is the elevator? [Lit: Where is the elevator?]", "Dov'è l'ascensore?"),
    ("It's very noisy [Lit: It is very noisy]", "È molto rumoroso"),
    ("Can you wake me up at 7? [Lit: Can-You wake-me at seven?]", "Può svegliarmi alle sette?"),
    ("Is there a safe in the room? [Lit: There is a safe-box in room?]", "C'è una cassaforte in camera?"),
    ("I had a great stay [Lit: Myself I found very-well]", "Mi sono trovato/a benissimo"),

    # --- 9. TIME, DATES & WEATHER ---
    ("What time is it? [Lit: What hour is?]", "Che ora è?"),
    ("It is one o'clock [Lit: It is the one]", "È l'una"),
    ("It is two / three / four o'clock [Lit: They are the two / three / four]", "Sono le due / tre / quattro"),
    ("Today [Lit: Today]", "Oggi"),
    ("Tomorrow [Lit: Tomorrow]", "Domani"),
    ("Yesterday [Lit: Yesterday]", "Ieri"),
    ("Tonight / This evening [Lit: This-evening]", "Stasera"),
    ("This morning [Lit: This-morning]", "Stamattina"),
    ("Afternoon [Lit: After-noon]", "Pomeriggio"),
    ("Now [Lit: Now]", "Adesso"),
    ("Later [Lit: More late]", "Più tardi"),
    ("Before [Lit: Before]", "Prima"),
    ("After [Lit: After]", "Dopo"),
    ("Early / Soon [Lit: Early]", "Presto"),
    ("Late [Lit: Late]", "Tardi"),
    ("The weekend [Lit: The end week]", "Il fine settimana"),
    ("What day is today? [Lit: What day is today?]", "Che giorno è oggi?"),
    ("At what time? [Lit: At what hour?]", "A che ora?"),
    ("In a short while [Lit: Between little]", "Tra poco"),
    ("Always / Never [Lit: Always / Never]", "Sempre / Mai"),
    ("See you tomorrow [Lit: To tomorrow]", "A domani"),
    ("Yesterday evening [Lit: Yesterday evening]", "Ieri sera"),
    ("Next week [Lit: The week next]", "La settimana prossima"),
    ("Last week [Lit: The week last]", "La settimana scorsa"),
    ("What's the weather like? [Lit: What weather makes-it?]", "Che tempo fa?"),
    ("It's nice weather [Lit: It makes beautiful weather]", "Fa bel tempo"),
    ("It's cold / hot [Lit: It makes cold / hot]", "Fa freddo / caldo"),
    ("It's raining [Lit: It stays raining]", "Sta piovendo"),
    ("It's sunny [Lit: There is the sun]", "C'è il sole"),
    ("It's windy [Lit: There is wind]", "C'è vento"),

    # --- 10. EMERGENCIES, MEDICAL & SAFETY ---
    ("Help! [Lit: Help!]", "Aiuto!"),
    ("Call the police! [Lit: Call-You the police!]", "Chiami la polizia!"),
    ("Call an ambulance! [Lit: Call-You an ambulance!]", "Chiami un'ambulanza!"),
    ("I need a doctor [Lit: I have need of a doctor]", "Ho bisogno di un medico"),
    ("Where is the hospital? [Lit: Where is the hospital?]", "Dov'è l'ospedale?"),
    ("Where is the pharmacy? [Lit: Where is the pharmacy?]", "Dov'è la farmacia?"),
    ("I feel sick [Lit: Myself I feel ill]", "Mi sento male"),
    ("I have pain here [Lit: I have pain here]", "Ho dolore qui"),
    ("Watch out! / Be careful! [Lit: Attentive!]", "Attento! / Attenta!"),
    ("I lost my passport [Lit: I have lost the my passport]", "Ho perso il mio passaporto"),
    ("I lost my phone [Lit: I have lost the phone]", "Ho perso il telefono"),
    ("There has been an accident [Lit: There has been an accident]", "C'è stato un incidente"),
    ("Emergency [Lit: Emergency]", "Emergenza"),
    ("I am unwell [Lit: I stay ill]", "Sto male"),
    ("Go away! [Lit: Go away!]", "Vai via!"),
    ("I was robbed [Lit: I was robbed]", "Sono stato/a derubato/a"),
    ("Where is the police station? [Lit: Where is the police-station?]", "Dov'è la questura?"),
    ("I have a fever [Lit: I have the fever]", "Ho la febbre"),
    ("I need medicine for... [Lit: I have need of a medicine for...]", "Ho bisogno di una medicina per..."),
    ("I am allergic to penicillin [Lit: I am allergic to-the penicillin]", "Sono allergico/a alla penicillina"),
    ("My head hurts [Lit: To-me makes pain the head]", "Mi fa male la testa"),
    ("My stomach hurts [Lit: To-me makes pain the stomach]", "Mi fa male lo stomaco"),
    ("Call a doctor, please [Lit: Call-You a doctor, for favor]", "Chiami un medico, per favore"),
    ("Stop, thief! [Lit: To-the thief!]", "Al ladro!"),
    ("I lost my wallet [Lit: I have lost the wallet]", "Ho perso il portafoglio"),

    # --- 11. TECHNOLOGY & PHONES ---
    ("Is there Wi-Fi here? [Lit: There is the Wi-Fi here?]", "C'è il Wi-Fi qui?"),
    ("Can I charge my phone here? [Lit: Can-I to-charge the phone here?]", "Posso caricare il telefono qui?"),
    ("Do you have a phone charger? [Lit: Hast-thou a battery-charger?]", "Hai un caricabatterie?"),
    ("Where can I buy a SIM card? [Lit: Where can-I to-buy a SIM?]", "Dove posso comprare una SIM?"),
    ("There is no signal [Lit: Not there is field]", "Non c'è campo"),
    ("My phone is dead [Lit: The my phone is discharged]", "Il mio telefono è scarico"),
    ("What is the phone number? [Lit: Which is the number of phone?]", "Qual è il numero di telefono?"),
    ("Can I take a picture? [Lit: Can-I to-make a photo?]", "Posso fare una foto?"),
    ("Would you take a picture of us? [Lit: To-us makes-You a photo, for favor?]", "Ci fa una foto, per favore?"),
    ("Send me a message [Lit: Send-me a message]", "Mandami un messaggio"),

    # --- 12. EXPRESSING OPINIONS, FEELINGS & NEEDS ---
    ("I like it [Lit: To-me it pleases]", "Mi piace"),
    ("I don't like it [Lit: Not to-me it pleases]", "Non mi piace"),
    ("I love it! [Lit: It I adore! / To-me it pleases very-much!]", "Lo adoro! / Mi piace tantissimo!"),
    ("I agree [Lit: I am of agreement]", "Sono d'accordo"),
    ("I disagree [Lit: Not I am of agreement]", "Non sono d'accordo"),
    ("I think that... [Lit: I think that...]", "Penso che..."),
    ("In my opinion [Lit: According to me]", "Secondo me"),
    ("I need... [Lit: I have need of...]", "Ho bisogno di..."),
    ("I want... [Lit: I want...]", "Voglio..."),
    ("I don't care [Lit: Not to-me of-it matters]", "Non me ne importa"),
    ("I'm tired [Lit: I am tired]", "Sono stanco/a"),
    ("I'm hungry [Lit: I have hunger]", "Ho fame"),
    ("I'm thirsty [Lit: I have thirst]", "Ho sete"),
    ("I'm cold / hot [Lit: I have cold / heat]", "Ho freddo / caldo"),
    ("I'm sleepy [Lit: I have sleepiness]", "Ho sonno"),
    ("I'm busy [Lit: I am occupied]", "Sono occupato/a"),
    ("I'm ready [Lit: I am ready]", "Sono pronto/a"),
    ("I am happy [Lit: I am happy]", "Sono contento/a"),
    ("I am sad [Lit: I am sad]", "Sono triste"),
    ("Don't worry [Lit: Not thyself worry-thou / Not Yourself worry-You]", "Non ti preoccupare / Non si preoccupi"),

    # --- 13. IDIOMS, SLANG & EXPRESSIONS ---
    ("How wonderful! [Lit: What beautiful!]", "Che bello!"),
    ("What a pity! / What a shame! [Lit: What sin/pity!]", "Che peccato!"),
    ("Oh my goodness! [Lit: My mama!]", "Mamma mia!"),
    ("Good luck! [Lit: Into mouth of-the wolf!]", "In bocca al lupo!"),
    ("Response to 'In bocca al lupo' [Lit: May-he die, the wolf!]", "Crepi il lupo!"),
    ("Makes sense / Sounds good [Lit: There it stays]", "Ci sta"),
    ("Thank goodness! [Lit: Less bad!]", "Meno male!"),
    ("I wish! / If only! [Lit: Maybe! / If only!]", "Magari!"),
    ("Come on! / Stop it! [Lit: Give!]", "Dai!"),
    ("I don't know / Beats me! [Lit: (Sound of indifference)]", "Boh!"),
    ("I can't wait [Lit: Not I see the hour]", "Non vedo l'ora"),
    ("To be in a bad mood [Lit: To have the moon crooked]", "Avere la luna storta"),
    ("To kill two birds with one stone [Lit: To take two pigeons with one fava-bean]", "Prendere due piccioni con una fava"),
    ("The sweetness of doing nothing [Lit: The sweet doing nothing]", "La dolce far niente"),
    ("What a mess! [Lit: What casino/mess!]", "Che casino!"),
    ("Are you kidding? [Lit: But art-thou joking?]", "Ma stai scherzando?"),
    ("Whatever! / Forget it! [Lit: Leave to lose!]", "Lascia perdere!"),
    ("Exactly! [Lit: Exact!]", "Esatto!"),
    ("Fingers crossed! [Lit: We cross the fingers!]", "Incrociamo le dita!"),
    ("To cost an arm and a leg [Lit: To cost an eye of-the head]", "Costare un occhio della testa"),
    ("To hit the nail on the head [Lit: To hit in-the mark]", "Colpire nel segno"),
    ("It's not a big deal [Lit: Not it is the end of-the world]", "Non è la fine del mondo"),
    ("Out of the blue [Lit: At the sudden]", "All'improvviso"),
    ("Speak of the devil [Lit: Speak-thou of-the devil and sprout-they the horns]", "Parli del diavolo e spuntano le corna"),
    ("I'm exhausted / dead tired [Lit: I am destroyed]", "Sono distrutto/a")
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
    num_pairs = st.sidebar.slider("Number of word pairs:", 10, len(italian_set), 30, step=1)
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
        st.session_state.matched_history = []  # Stores ordered tuples: (english, italian, team_idx)
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
