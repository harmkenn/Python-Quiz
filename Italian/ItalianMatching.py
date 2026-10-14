import streamlit as st
import random

# --- Page Setup ---
if __name__ == "__main__":
    st.set_page_config(page_title="Italian Match", layout="wide")

# --- Load custom phrase set with Word-for-Word literal translations ---
ITALIAN_PHRASES = [
    # --- 1. BASIC GREETINGS & FORMALITIES ---
    ("Hi / Bye", "Ciao"),
    ("Good morning / Good day <br>[Good day]", "Buongiorno"),
    ("Good evening <br>[Good evening]", "Buonasera"),
    ("Good night <br>[Good night]", "Buonanotte"),
    ("Hello (polite / neutral) <br>[Safe/Healthy]", "Salve"),
    ("Goodbye <br>[Until seeing each other again]", "Arrivederci"),
    ("See you soon <br>[To soon]", "A presto"),
    ("See you later <br>[To after]", "A dopo"),
    ("See you <br>[Us we see]", "Ci vediamo"),
    ("Please <br>[For favor]", "Per favore"),
    ("Thank you <br>[Graces/Thanks]", "Grazie"),
    ("Thank you very much <br>[Thousand thanks]", "Grazie mille"),
    ("You're welcome <br>[I pray/ask]", "Prego"),
    ("It's nothing / Don't mention it <br>[Of nothing]", "Di niente"),
    ("Excuse me (formal) <br>[Excuse (you)]", "Scusi"),
    ("Excuse me / Sorry <br>[Excuse (thou)]", "Scusa"),
    ("Excuse me (to pass through) <br>[Permission]", "Permesso"),
    ("I'm sorry <br>[To me it displeases]", "Mi dispiace"),
    ("Yes", "Sì"),
    ("No", "No"),
    ("All right / OK <br>[It goes well]", "Va bene"),
    ("Pleased to meet you <br>[Pleasure]", "Piacere"),
    ("Welcome <br>[Well come]", "Benvenuto"),
    ("Have a good day <br>[Good day-duration]", "Buona giornata"),
    ("Have a good evening <br>[Good evening-duration]", "Buona serata"),
    ("Have a good trip <br>[Good voyage]", "Buon viaggio"),
    ("Have a good weekend <br>[Good end week]", "Buon fine settimana"),
    ("Have fun! <br>[Good fun!]", "Buon divertimento!"),
    ("Happy birthday! <br>[Good birthday!]", "Buon compleanno!"),
    ("Congratulations! <br>[Congratulations!]", "Congratulazioni!"),

    # --- 2. GETTING TO KNOW SOMEONE & SMALL TALK ---
    ("How are you? (formal) <br>[How stay (you)]", "Come sta?"),
    ("How are you? (informal) <br>[How stay (thou)]", "Come stai?"),
    ("How's it going? <br>[How goes?]", "Come va?"),
    ("I'm doing well, thank you <br>[I stay well, thanks]", "Sto bene, grazie"),
    ("And you? (formal) <br>[And You?]", "E Lei?"),
    ("And you? (informal) <br>[And thou?]", "E tu?"),
    ("What is your name? (informal) <br>[How yourself call-you?]", "Come ti chiami?"),
    ("What is your name? (formal) <br>[How yourself call-You?]", "Come si chiama?"),
    ("My name is... <br>[Myself I call...]", "Mi chiamo..."),
    ("Where are you from? (informal) <br>[Of where art-thou?]", "Di dove sei?"),
    ("Where are you from? (formal) <br>[Of where is-You?]", "Di dov'è?"),
    ("I am from... <br>[I am of...]", "Sono di..."),
    ("How old are you? <br>[How many years have-thou?]", "Quanti anni hai?"),
    ("I am ... years old <br>[I have ... years]", "Ho ... anni"),
    ("What do you do for a living? <br>[What do-thou in the life?]", "Cosa fai nella vita?"),
    ("What's up? <br>[What self says?]", "Cosa si dice?"),
    ("Everything is good <br>[All well]", "Tutto bene"),
    ("Not bad <br>[Not there is bad]", "Non c'è male"),
    ("So-so <br>[Like this like this]", "Così così"),
    ("Where do you live? <br>[Where live-thou?]", "Dove abiti?"),
    ("I live in... <br>[I live at...]", "Abito a..."),
    ("Are you here on vacation? <br>[Art-thou here in vacation?]", "Sei qui in vacanza?"),
    ("I am here for work <br>[I am here for work]", "Sono qui per lavoro"),
    ("Do you have family here? <br>[Hast-thou family here?]", "Hai famiglia qui?"),
    ("I am traveling alone <br>[I stay traveling from alone]", "Sto viaggiando da solo/a"),
    ("Who are you with? <br>[With whom art-thou?]", "Con chi sei?"),
    ("I am here with my family <br>[I am here with the my family]", "Sono qui con la mia famiglia"),
    ("I am here with friends <br>[I am here with of the friends]", "Sono qui con degli amici"),
    ("Nice to talk to you <br>[It was a pleasure to talk with thee]", "È stato un piacere parlare con te"),
    ("Let's keep in touch <br>[Hold ourselves in contact]", "Teniamoci in contatto"),

    # --- 3. LANGUAGE & COMMUNICATION ---
    ("Do you speak English? (informal) <br>[Speak-thou English?]", "Parli inglese?"),
    ("Do you speak English? (formal) <br>[Speaks-You English?]", "Parla inglese?"),
    ("I speak a little Italian <br>[I speak a little of Italian]", "Parlo un po' di italiano"),
    ("I don't speak Italian <br>[Not I speak Italian]", "Non parlo italiano"),
    ("I don't understand <br>[Not I understand]", "Non capisco"),
    ("I understand <br>[I understand]", "Capisco"),
    ("Can you speak more slowly? <br>[Can-You speak more slowly?]", "Può parlare più lentamente?"),
    ("Can you repeat that? <br>[Can-thou repeat?]", "Puoi ripetere?"),
    ("How do you say ... in Italian? <br>[How self says ... in Italian?]", "Come si dice ... in italiano?"),
    ("What does that mean? <br>[What thing signifies?]", "Che cosa significa?"),
    ("Could you write it down, please? <br>[Can-You write it, for favor?]", "Può scriverlo, per favore?"),
    ("How do you spell it? <br>[How self writes?]", "Come si scrive?"),
    ("I am learning Italian <br>[I stay learning the Italian]", "Sto imparando l'italiano"),
    ("I got it / I understood <br>[I have understood]", "Ho capito"),
    ("I didn't get it <br>[Not I have understood]", "Non ho capito"),
    ("Can you help me? (formal) <br>[Can-You help me?]", "Può aiutarmi?"),
    ("Can you help me? (informal) <br>[Can-thou help me?]", "Puoi aiutarmi?"),
    ("What did you say? (formal) <br>[What has-You said?]", "Cosa ha detto?"),
    ("What did you say? (informal) <br>[What hast-thou said?]", "Cosa hai detto?"),
    ("I have a question <br>[I have a question]", "Ho una domanda"),
    ("No problem <br>[No problem]", "Nessun problema"),
    ("It doesn't matter / Never mind <br>[Not imports]", "Non importa"),
    ("I don't know <br>[Not it I know]", "Non lo so"),
    ("I am sure of it <br>[Of it I am sure]", "Ne sono sicuro/a"),
    ("Are you sure? <br>[Art-thou sure?]", "Sei sicuro/a?"),
    ("What is this called? <br>[How self calls this?]", "Come si chiama questo?"),
    ("Could you speak a bit louder? <br>[Can-thou speak a bit more strong?]", "Puoi parlare un po' più forte?"),
    ("My Italian is not very good <br>[The my Italian not is very good]", "Il mio italiano non è molto buono"),
    ("I understand a bit, but I can't speak well <br>[I understand a bit, but not I speak well]", "Capisco un po', ma non parlo bene"),
    ("Thanks for your patience <br>[Thanks for the patience]", "Grazie per la pazienza"),

    # --- 4. NAVIGATION & DIRECTIONS ---
    ("Where is... ? <br>[Where is...?]", "Dov'è...?"),
    ("Where are...? <br>[Where are...?]", "Dove sono...?"),
    ("Where is the bathroom? <br>[Where is the bath?]", "Dov'è il bagno?"),
    ("Where is the station? <br>[Where is the station?]", "Dov'è la stazione?"),
    ("Where is the bus stop? <br>[Where is the stop of the bus?]", "Dov'è la fermata dell'autobus?"),
    ("To the right <br>[At right]", "A destra"),
    ("To the left <br>[At left]", "A sinistra"),
    ("Straight ahead <br>[Straight]", "Dritto"),
    ("Straight on / Keep going straight <br>[Always straight]", "Sempre dritto"),
    ("At the corner <br>[At the corner]", "All'angolo"),
    ("Near <br>[Near]", "Vicino"),
    ("Far <br>[Far]", "Lontano"),
    ("Here <br>[Here]", "Qui"),
    ("There <br>[There / There]", "Lì / Là"),
    ("Opposite / Facing <br>[Of front to]", "Di fronte a"),
    ("Next to <br>[Alongside to]", "Accanto a"),
    ("How do I get to...? <br>[How arrive-I to...?]", "Come arrivo a...?"),
    ("Is it nearby? <br>[Is near?]", "È vicino?"),
    ("Is it far from here? <br>[Is far from here?]", "È lontano da qui?"),
    ("I am lost <br>[Myself I am lost]", "Mi sono perso / persa"),
    ("Where is the entrance? <br>[Where is the entry?]", "Dov'è l'ingresso?"),
    ("Where is the exit? <br>[Where is the exit?]", "Dov'è l'uscita?"),
    ("Cross the street <br>[Cross the street]", "Attraversa la strada"),
    ("Turn right at the traffic light <br>[Turn at right at the traffic-light]", "Gira a destra al semaforo"),
    ("Take the first street on the left <br>[Take the first street at left]", "Prendi la prima strada a sinistra"),
    ("Behind the building <br>[Behind the building]", "Dietro l'edificio"),
    ("In front of the church <br>[Before at the church]", "Davanti alla chiesa"),
    ("Between the two shops <br>[Between the two shops]", "Tra i due negozi"),
    ("How many minutes on foot? <br>[How many minutes at feet?]", "Quanti minuti a piedi?"),
    ("Is it safe to walk here? <br>[Is safe to walk here?]", "È sicuro camminare qui?"),

    # --- 5. TRAVEL, TRANSPORT & TICKETS ---
    ("Which platform? <br>[Which track?]", "Quale binario?"),
    ("A ticket to..., please <br>[A ticket for..., for favor]", "Un biglietto per..., per favore"),
    ("One way or round trip? <br>[Only going or return?]", "Solo andata o ritorno?"),
    ("When does the train leave? <br>[When departs the train?]", "Quando parte il treno?"),
    ("When does the bus arrive? <br>[When arrives the bus?]", "Quando arriva l'autobus?"),
    ("Is this seat free? <br>[Is free this seat?]", "È libero questo posto?"),
    ("Where can I validate my ticket? <br>[Where can-I to-validate the ticket?]", "Dove posso convalidare il biglietto?"),
    ("Is there a delay? <br>[There is a delay?]", "C'è un ritardo?"),
    ("Which bus goes to the center? <br>[Which bus goes in center?]", "Quale autobus va in centro?"),
    ("Where do I get off? <br>[Where must-I to-descend?]", "Dove devo scendere?"),
    ("I need a taxi <br>[I have need of a taxi]", "Ho bisogno di un taxi"),
    ("Please take me to this address <br>[Me carry-You to this address, for favor]", "Mi porti a questo indirizzo, per favore"),
    ("How much to go to the airport? <br>[How much costs to go to the airport?]", "Quanto costa andare all'aeroporto?"),
    ("Stop here, please <br>[Yourself stop-You here, for favor]", "Si fermi qui, per favore"),
    ("Where is the baggage claim? <br>[Where is the withdrawal bags?]", "Dov'è il ritiro bagagli?"),
    ("My luggage is lost <br>[The my baggage is lost]", "Il mio bagaglio è smarrito"),
    ("I need to rent a car <br>[Must-I to-rent a car]", "Devo noleggiare un'auto"),
    ("Where can I park? <br>[Where can-I to-park?]", "Dove posso parcheggiare?"),
    ("Is parking free? <br>[The parking is free?]", "Il parcheggio è gratuito?"),
    ("Does this train stop in...? <br>[This train stops in...?]", "Questo treno ferma a...?"),

    # --- 6. DINING & DRINKING ---
    ("A table for two, please <br>[A table for two, for favor]", "Un tavolo per due, per favore"),
    ("Can I see the menu? <br>[Can-I to-see the menu?]", "Posso vedere il menu?"),
    ("I would like to order <br>[I would wish to order]", "Vorrei ordinare"),
    ("I would like... <br>[I would wish...]", "Vorrei..."),
    ("I'll have... <br>[I take...]", "Prendo..."),
    ("What do you recommend? <br>[What thing to us recommend-You?]", "Che cosa ci consiglia?"),
    ("What is the dish of the day? <br>[Which is the dish of the day?]", "Qual è il piatto del giorno?"),
    ("An espresso, please <br>[A coffee, for favor]", "Un caffè, per favore"),
    ("A cappuccino, please <br>[A cappuccino, for favor]", "Un cappuccio, per favore"),
    ("A glass of water, please <br>[A glass of water, for favor]", "Un bicchiere d'acqua, per favore"),
    ("Still or sparkling water? <br>[Water natural or sparkling?]", "Acqua naturale o frizzante?"),
    ("House wine <br>[Wine of the house]", "Vino della casa"),
    ("A beer, please <br>[A beer, for favor]", "Una birra, per favore"),
    ("The bill, please <br>[The account, for favor]", "Il conto, per favore"),
    ("Can I pay by card? <br>[Can-I to-pay with the card?]", "Posso pagare con la carta?"),
    ("Do you accept credit cards? <br>[Accept-you cards of credit?]", "Accettate carte di credito?"),
    ("In cash <br>[In cash-money]", "In contanti"),
    ("It's my treat / I'm paying <br>[Offer I]", "Offro io"),
    ("Keep the change <br>[Keep-You the remainder]", "Tenga il resto"),
    ("It’s delicious! <br>[It is delicious!]", "È delizioso!"),
    ("It is very good <br>[It is very good]", "È molto buono"),
    ("I am vegetarian <br>[I am vegetarian]", "Sono vegetariano/a"),
    ("I am vegan <br>[I am vegan]", "Sono vegano/a"),
    ("I am allergic to... <br>[I am allergic to...]", "Sono allergico/a a..."),
    ("Gluten-free <br>[Without gluten]", "Senza glutine"),
    ("Cheers! <br>[Health!]", "Salute!"),
    ("Enjoy your meal! <br>[Good appetite!]", "Buon appetito!"),
    ("That's enough, thank you <br>[Enough like this, thanks]", "Basta così, grazie"),
    ("Where is the rest room? <br>[Where is the toilet?]", "Dov'è la toilette?"),
    ("Can we have split bills? <br>[Can-we to-have two accounts separated?]", "Possiamo avere due conti separati?"),
    ("A glass of red / white wine <br>[A glass of wine red / white]", "Un bicchiere di vino rosso / bianco"),
    ("Without ice, please <br>[Without ice, for favor]", "Senza ghiaccio, per favore"),
    ("Could we have some bread? <br>[Can-we to-have of the bread?]", "Possiamo avere del pane?"),
    ("Is service included? <br>[The service is included?]", "Il servizio è incluso?"),
    ("I didn't order this <br>[Not I have ordered this]", "Non ho ordinato questo"),
    ("Is it spicy? <br>[Is spicy?]", "È piccante?"),
    ("Another one, please <br>[An other, for favor]", "Un altro, per favore"),
    ("Can I have a receipt? <br>[Can-I to-have the receipt?]", "Posso avere la ricevuta?"),
    ("Is there a cover charge? <br>[There is the cover-charge?]", "C'è il coperto?"),
    ("To go / Takeaway <br>[From transport]", "Da asporto"),

    # --- 7. SHOPPING & MONEY ---
    ("How much does it cost? <br>[How much costs?]", "Quanto costa?"),
    ("How much do these cost? <br>[How much cost-they?]", "Quanto costano?"),
    ("It is too expensive <br>[It is too dear]", "È troppo caro"),
    ("Is there a discount? <br>[There is a discount?]", "C'è uno sconto?"),
    ("I'm just looking, thank you <br>[I stay only looking, thanks]", "Sto solo guardando, grazie"),
    ("Can I try it on? <br>[Can-I to-try-it?]", "Posso provarlo?"),
    ("Where is the fitting room? <br>[Where is the dressing-room?]", "Dov'è il camerino?"),
    ("Do you have a larger / smaller size? <br>[Have-You a size more big / small?]", "Ha una taglia più grande / piccola?"),
    ("I'll take it <br>[It I take]", "Lo prendo"),
    ("I don't want it <br>[Not it I want]", "Non lo voglio"),
    ("Do you have...? <br>[Have-you...?]", "Avete...?"),
    ("What time do you close? <br>[At what hour close-you?]", "A che ora chiudete?"),
    ("What time do you open? <br>[At what hour open-you?]", "A che ora aprite?"),
    ("Is it open? <br>[Is open?]", "È aperto?"),
    ("Is it closed? <br>[Is closed?]", "È chiuso?"),
    ("Where is the ATM? <br>[Where is the bank-machine?]", "Dov'è il bancomat?"),
    ("Receipt, please <br>[Receipt, for favor]", "Scontrino, per favore"),
    ("Can I have a bag? <br>[Can-I to-have a bag?]", "Posso avere un sacchetto?"),
    ("Do you have my size? <br>[Have-you the my size?]", "Avete la mia taglia?"),
    ("What brand is it? <br>[What brand is?]", "Che marca è?"),
    ("Can we pay separately? <br>[Can-we to-pay separately?]", "Possiamo pagare separatamente?"),
    ("Do you have change? <br>[Have-you the remainder?]", "Avete il resto?"),
    ("Is it on sale? <br>[Is in sale/discount?]", "È in saldo?"),
    ("Where can I buy...? <br>[Where can-I to-buy...?]", "Dove posso comprare...?"),
    ("It's good quality <br>[It is of good quality]", "È di buona qualità"),
    ("I'm looking for... <br>[I stay searching...]", "Sto cercando..."),
    ("Can I pay with contactless? <br>[Can-I to-pay contactless?]", "Posso pagare contactless?"),
    ("Do you have another color? <br>[Of it have-you an other color?]", "Ne avete un altro colore?"),
    ("Can I exchange this? <br>[Can-I to-change-it?]", "Posso cambiarlo?"),
    ("I'd like a refund <br>[I would wish a refund]", "Vorrei un rimborso"),

    # --- 8. ACCOMMODATIONS & HOTELS ---
    ("I have a reservation <br>[I have a reservation]", "Ho una prenotazione"),
    ("Under the name... <br>[At name of...]", "A nome di..."),
    ("Do you have a vacant room? <br>[Have-you a room free?]", "Avete una camera libera?"),
    ("For how many nights? <br>[For how-many nights?]", "Per quante notti?"),
    ("For one night / two nights <br>[For one night / two nights]", "Per una notte / due notti"),
    ("Single / Double room <br>[Room single / double]", "Camera singola / doppia"),
    ("With a double bed <br>[With bed matrimonial]", "Con letto matrimoniale"),
    ("Is breakfast included? <br>[The breakfast is included?]", "La colazione è inclusa?"),
    ("What time is check-out? <br>[At what hour is the check-out?]", "A che ora è il check-out?"),
    ("Can I leave my luggage here? <br>[Can-I to-leave the baggages here?]", "Posso lasciare i bagagli qui?"),
    ("The key, please <br>[The key, for favor]", "La chiave, per favore"),
    ("The air conditioning doesn't work <br>[The air conditioned not works]", "L'aria condizionata non funziona"),
    ("There is no hot water <br>[Not there is water hot]", "Non c'è acqua calda"),
    ("What is the Wi-Fi password? <br>[Which is the password of the Wi-Fi?]", "Qual è la password del Wi-Fi?"),
    ("Could I have an extra towel? <br>[Can-I to-have a towel in more?]", "Posso avere un asciugamano in più?"),
    ("Where is the elevator? <br>[Where is the elevator?]", "Dov'è l'ascensore?"),
    ("It's very noisy <br>[It is very noisy]", "È molto rumoroso"),
    ("Can you wake me up at 7? <br>[Can-You wake-me at seven?]", "Può svegliarmi alle sette?"),
    ("Is there a safe in the room? <br>[There is a safe-box in room?]", "C'è una cassaforte in camera?"),
    ("I had a great stay <br>[Myself I found very-well]", "Mi sono trovato/a benissimo"),

    # --- 9. TIME, DATES & WEATHER ---
    ("What time is it? <br>[What hour is?]", "Che ora è?"),
    ("It is one o'clock <br>[It is the one]", "È l'una"),
    ("It is two / three / four o'clock <br>[They are the two / three / four]", "Sono le due / tre / quattro"),
    ("Today <br>[Today]", "Oggi"),
    ("Tomorrow <br>[Tomorrow]", "Domani"),
    ("Yesterday <br>[Yesterday]", "Ieri"),
    ("Tonight / This evening <br>[This-evening]", "Stasera"),
    ("This morning <br>[This-morning]", "Stamattina"),
    ("Afternoon <br>[After-noon]", "Pomeriggio"),
    ("Now <br>[Now]", "Adesso"),
    ("Later <br>[More late]", "Più tardi"),
    ("Before <br>[Before]", "Prima"),
    ("After <br>[After]", "Dopo"),
    ("Early / Soon <br>[Early]", "Presto"),
    ("Late <br>[Late]", "Tardi"),
    ("The weekend <br>[The end week]", "Il fine settimana"),
    ("What day is today? <br>[What day is today?]", "Che giorno è oggi?"),
    ("At what time? <br>[At what hour?]", "A che ora?"),
    ("In a short while <br>[Between little]", "Tra poco"),
    ("Always / Never <br>[Always / Never]", "Sempre / Mai"),
    ("See you tomorrow <br>[To tomorrow]", "A domani"),
    ("Yesterday evening <br>[Yesterday evening]", "Ieri sera"),
    ("Next week <br>[The week next]", "La settimana prossima"),
    ("Last week <br>[The week last]", "La settimana scorsa"),
    ("What's the weather like? <br>[What weather makes-it?]", "Che tempo fa?"),
    ("It's nice weather <br>[It makes beautiful weather]", "Fa bel tempo"),
    ("It's cold / hot <br>[It makes cold / hot]", "Fa freddo / caldo"),
    ("It's raining <br>[It stays raining]", "Sta piovendo"),
    ("It's sunny <br>[There is the sun]", "C'è il sole"),
    ("It's windy <br>[There is wind]", "C'è vento"),

    # --- 10. EMERGENCIES, MEDICAL & SAFETY ---
    ("Help! <br>[Help!]", "Aiuto!"),
    ("Call the police! <br>[Call-You the police!]", "Chiami la polizia!"),
    ("Call an ambulance! <br>[Call-You an ambulance!]", "Chiami un'ambulanza!"),
    ("I need a doctor <br>[I have need of a doctor]", "Ho bisogno di un medico"),
    ("Where is the hospital? <br>[Where is the hospital?]", "Dov'è l'ospedale?"),
    ("Where is the pharmacy? <br>[Where is the pharmacy?]", "Dov'è la farmacia?"),
    ("I feel sick <br>[Myself I feel ill]", "Mi sento male"),
    ("I have pain here <br>[I have pain here]", "Ho dolore qui"),
    ("Watch out! / Be careful! <br>[Attentive!]", "Attento! / Attenta!"),
    ("I lost my passport <br>[I have lost the my passport]", "Ho perso il mio passaporto"),
    ("I lost my phone <br>[I have lost the phone]", "Ho perso il telefono"),
    ("There has been an accident <br>[There has been an accident]", "C'è stato un incidente"),
    ("Emergency <br>[Emergency]", "Emergenza"),
    ("I am unwell <br>[I stay ill]", "Sto male"),
    ("Go away! <br>[Go away!]", "Vai via!"),
    ("I was robbed <br>[I was robbed]", "Sono stato/a derubato/a"),
    ("Where is the police station? <br>[Where is the police-station?]", "Dov'è la questura?"),
    ("I have a fever <br>[I have the fever]", "Ho la febbre"),
    ("I need medicine for... <br>[I have need of a medicine for...]", "Ho bisogno di una medicina per..."),
    ("I am allergic to penicillin <br>[I am allergic to-the penicillin]", "Sono allergico/a alla penicillina"),
    ("My head hurts <br>[To-me makes pain the head]", "Mi fa male la testa"),
    ("My stomach hurts <br>[To-me makes pain the stomach]", "Mi fa male lo stomaco"),
    ("Call a doctor, please <br>[Call-You a doctor, for favor]", "Chiami un medico, per favore"),
    ("Stop, thief! <br>[To-the thief!]", "Al ladro!"),
    ("I lost my wallet <br>[I have lost the wallet]", "Ho perso il portafoglio"),

    # --- 11. TECHNOLOGY & PHONES ---
    ("Is there Wi-Fi here? <br>[There is the Wi-Fi here?]", "C'è il Wi-Fi qui?"),
    ("Can I charge my phone here? <br>[Can-I to-charge the phone here?]", "Posso caricare il telefono qui?"),
    ("Do you have a phone charger? <br>[Hast-thou a battery-charger?]", "Hai un caricabatterie?"),
    ("Where can I buy a SIM card? <br>[Where can-I to-buy a SIM?]", "Dove posso comprare una SIM?"),
    ("There is no signal <br>[Not there is field]", "Non c'è campo"),
    ("My phone is dead <br>[The my phone is discharged]", "Il mio telefono è scarico"),
    ("What is the phone number? <br>[Which is the number of phone?]", "Qual è il numero di telefono?"),
    ("Can I take a picture? <br>[Can-I to-make a photo?]", "Posso fare una foto?"),
    ("Would you take a picture of us? <br>[To-us makes-You a photo, for favor?]", "Ci fa una foto, per favore?"),
    ("Send me a message <br>[Send-me a message]", "Mandami un messaggio"),

    # --- 12. EXPRESSING OPINIONS, FEELINGS & NEEDS ---
    ("I like it <br>[To-me it pleases]", "Mi piace"),
    ("I don't like it <br>[Not to-me it pleases]", "Non mi piace"),
    ("I love it! <br>[It I adore! / To-me it pleases very-much!]", "Lo adoro! / Mi piace tantissimo!"),
    ("I agree <br>[I am of agreement]", "Sono d'accordo"),
    ("I disagree <br>[Not I am of agreement]", "Non sono d'accordo"),
    ("I think that... <br>[I think that...]", "Penso che..."),
    ("In my opinion <br>[According to me]", "Secondo me"),
    ("I need... <br>[I have need of...]", "Ho bisogno di..."),
    ("I want... <br>[I want...]", "Voglio..."),
    ("I don't care <br>[Not to-me of-it matters]", "Non me ne importa"),
    ("I'm tired <br>[I am tired]", "Sono stanco/a"),
    ("I'm hungry <br>[I have hunger]", "Ho fame"),
    ("I'm thirsty <br>[I have thirst]", "Ho sete"),
    ("I'm cold / hot <br>[I have cold / heat]", "Ho freddo / caldo"),
    ("I'm sleepy <br>[I have sleepiness]", "Ho sonno"),
    ("I'm busy <br>[I am occupied]", "Sono occupato/a"),
    ("I'm ready <br>[I am ready]", "Sono pronto/a"),
    ("I am happy <br>[I am happy]", "Sono contento/a"),
    ("I am sad <br>[I am sad]", "Sono triste"),
    ("Don't worry <br>[Not thyself worry-thou / Not Yourself worry-You]", "Non ti preoccupare / Non si preoccupi"),

    # --- 13. IDIOMS, SLANG & EXPRESSIONS ---
    ("How wonderful! <br>[What beautiful!]", "Che bello!"),
    ("What a pity! / What a shame! <br>[What sin/pity!]", "Che peccato!"),
    ("Oh my goodness! <br>[My mama!]", "Mamma mia!"),
    ("Good luck! <br>[Into mouth of-the wolf!]", "In bocca al lupo!"),
    ("Response to 'In bocca al lupo' <br>[May-he die, the wolf!]", "Crepi il lupo!"),
    ("Makes sense / Sounds good <br>[There it stays]", "Ci sta"),
    ("Thank goodness! <br>[Less bad!]", "Meno male!"),
    ("I wish! / If only! <br>[Maybe! / If only!]", "Magari!"),
    ("Come on! / Stop it! <br>[Give!]", "Dai!"),
    ("I don't know / Beats me! <br>[(Sound of indifference)]", "Boh!"),
    ("I can't wait <br>[Not I see the hour]", "Non vedo l'ora"),
    ("To be in a bad mood <br>[To have the moon crooked]", "Avere la luna storta"),
    ("To kill two birds with one stone <br>[To take two pigeons with one fava-bean]", "Prendere due piccioni con una fava"),
    ("The sweetness of doing nothing <br>[The sweet doing nothing]", "La dolce far niente"),
    ("What a mess! <br>[What casino/mess!]", "Che casino!"),
    ("Are you kidding? <br>[But art-thou joking?]", "Ma stai scherzando?"),
    ("Whatever! / Forget it! <br>[Leave to lose!]", "Lascia perdere!"),
    ("Exactly! <br>[Exact!]", "Esatto!"),
    ("Fingers crossed! <br>[We cross the fingers!]", "Incrociamo le dita!"),
    ("To cost an arm and a leg <br>[To cost an eye of-the head]", "Costare un occhio della testa"),
    ("To hit the nail on the head <br>[To hit in-the mark]", "Colpire nel segno"),
    ("It's not a big deal <br>[Not it is the end of-the world]", "Non è la fine del mondo"),
    ("Out of the blue <br>[At the sudden]", "All'improvviso"),
    ("Speak of the devil <br>[Speak-thou of-the devil and sprout-they the horns]", "Parli del diavolo e spuntano le corna"),
    ("I'm exhausted / dead tired <br>[I am destroyed]", "Sono distrutto/a")
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
