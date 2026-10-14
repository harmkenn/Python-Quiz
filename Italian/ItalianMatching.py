import streamlit as st
import random

# --- Page Setup ---
if __name__ == "__main__":
    st.set_page_config(page_title="Italian Match", layout="wide")

# --- Load custom phrase set with Word-for-Word literal translations ---
ITALIAN_PHRASES = [
    # --- 1. BASIC GREETINGS & FORMALITIES ---
    ("Hi / Bye", "Ciao"),
    ("Good morning / Good day\n[Good day]", "Buongiorno"),
    ("Good evening\n[Good evening]", "Buonasera"),
    ("Good night\n[Good night]", "Buonanotte"),
    ("Hello (polite / neutral)\n[Safe/Healthy]", "Salve"),
    ("Goodbye\n[Until seeing each other again]", "Arrivederci"),
    ("See you soon\n[To soon]", "A presto"),
    ("See you later\n[To after]", "A dopo"),
    ("See you\n[Us we see]", "Ci vediamo"),
    ("Please\n[For favor]", "Per favore"),
    ("Thank you\n[Graces/Thanks]", "Grazie"),
    ("Thank you very much\n[Thousand thanks]", "Grazie mille"),
    ("You're welcome\n[I pray/ask]", "Prego"),
    ("It's nothing / Don't mention it\n[Of nothing]", "Di niente"),
    ("Excuse me (formal)\n[Excuse (you)]", "Scusi"),
    ("Excuse me / Sorry\n[Excuse (thou)]", "Scusa"),
    ("Excuse me (to pass through)\n[Permission]", "Permesso"),
    ("I'm sorry\n[To me it displeases]", "Mi dispiace"),
    ("Yes", "Sì"),
    ("No", "No"),
    ("All right / OK\n[It goes well]", "Va bene"),
    ("Pleased to meet you\n[Pleasure]", "Piacere"),
    ("Welcome\n[Well come]", "Benvenuto"),
    ("Have a good day\n[Good day-duration]", "Buona giornata"),
    ("Have a good evening\n[Good evening-duration]", "Buona serata"),
    ("Have a good trip\n[Good voyage]", "Buon viaggio"),
    ("Have a good weekend\n[Good end week]", "Buon fine settimana"),
    ("Have fun!\n[Good fun!]", "Buon divertimento!"),
    ("Happy birthday!\n[Good birthday!]", "Buon compleanno!"),
    ("Congratulations!\n[Congratulations!]", "Congratulazioni!"),

    # --- 2. GETTING TO KNOW SOMEONE & SMALL TALK ---
    ("How are you? (formal)\n[How stay (you)]", "Come sta?"),
    ("How are you? (informal)\n[How stay (thou)]", "Come stai?"),
    ("How's it going?\n[How goes?]", "Come va?"),
    ("I'm doing well, thank you\n[I stay well, thanks]", "Sto bene, grazie"),
    ("And you? (formal)\n[And You?]", "E Lei?"),
    ("And you? (informal)\n[And thou?]", "E tu?"),
    ("What is your name? (informal)\n[How yourself call-you?]", "Come ti chiami?"),
    ("What is your name? (formal)\n[How yourself call-You?]", "Come si chiama?"),
    ("My name is...\n[Myself I call...]", "Mi chiamo..."),
    ("Where are you from? (informal)\n[Of where art-thou?]", "Di dove sei?"),
    ("Where are you from? (formal)\n[Of where is-You?]", "Di dov'è?"),
    ("I am from...\n[I am of...]", "Sono di..."),
    ("How old are you?\n[How many years have-thou?]", "Quanti anni hai?"),
    ("I am ... years old\n[I have ... years]", "Ho ... anni"),
    ("What do you do for a living?\n[What do-thou in the life?]", "Cosa fai nella vita?"),
    ("What's up?\n[What self says?]", "Cosa si dice?"),
    ("Everything is good\n[All well]", "Tutto bene"),
    ("Not bad\n[Not there is bad]", "Non c'è male"),
    ("So-so\n[Like this like this]", "Così così"),
    ("Where do you live?\n[Where live-thou?]", "Dove abiti?"),
    ("I live in...\n[I live at...]", "Abito a..."),
    ("Are you here on vacation?\n[Art-thou here in vacation?]", "Sei qui in vacanza?"),
    ("I am here for work\n[I am here for work]", "Sono qui per lavoro"),
    ("Do you have family here?\n[Hast-thou family here?]", "Hai famiglia qui?"),
    ("I am traveling alone\n[I stay traveling from alone]", "Sto viaggiando da solo/a"),
    ("Who are you with?\n[With whom art-thou?]", "Con chi sei?"),
    ("I am here with my family\n[I am here with the my family]", "Sono qui con la mia famiglia"),
    ("I am here with friends\n[I am here with of the friends]", "Sono qui con degli amici"),
    ("Nice to talk to you\n[It was a pleasure to talk with thee]", "È stato un piacere parlare con te"),
    ("Let's keep in touch\n[Hold ourselves in contact]", "Teniamoci in contatto"),

    # --- 3. LANGUAGE & COMMUNICATION ---
    ("Do you speak English? (informal)\n[Speak-thou English?]", "Parli inglese?"),
    ("Do you speak English? (formal)\n[Speaks-You English?]", "Parla inglese?"),
    ("I speak a little Italian\n[I speak a little of Italian]", "Parlo un po' di italiano"),
    ("I don't speak Italian\n[Not I speak Italian]", "Non parlo italiano"),
    ("I don't understand\n[Not I understand]", "Non capisco"),
    ("I understand\n[I understand]", "Capisco"),
    ("Can you speak more slowly?\n[Can-You speak more slowly?]", "Può parlare più lentamente?"),
    ("Can you repeat that?\n[Can-thou repeat?]", "Puoi ripetere?"),
    ("How do you say ... in Italian?\n[How self says ... in Italian?]", "Come si dice ... in italiano?"),
    ("What does that mean?\n[What thing signifies?]", "Che cosa significa?"),
    ("Could you write it down, please?\n[Can-You write it, for favor?]", "Può scriverlo, per favore?"),
    ("How do you spell it?\n[How self writes?]", "Come si scrive?"),
    ("I am learning Italian\n[I stay learning the Italian]", "Sto imparando l'italiano"),
    ("I got it / I understood\n[I have understood]", "Ho capito"),
    ("I didn't get it\n[Not I have understood]", "Non ho capito"),
    ("Can you help me? (formal)\n[Can-You help me?]", "Può aiutarmi?"),
    ("Can you help me? (informal)\n[Can-thou help me?]", "Puoi aiutarmi?"),
    ("What did you say? (formal)\n[What has-You said?]", "Cosa ha detto?"),
    ("What did you say? (informal)\n[What hast-thou said?]", "Cosa hai detto?"),
    ("I have a question\n[I have a question]", "Ho una domanda"),
    ("No problem\n[No problem]", "Nessun problema"),
    ("It doesn't matter / Never mind\n[Not imports]", "Non importa"),
    ("I don't know\n[Not it I know]", "Non lo so"),
    ("I am sure of it\n[Of it I am sure]", "Ne sono sicuro/a"),
    ("Are you sure?\n[Art-thou sure?]", "Sei sicuro/a?"),
    ("What is this called?\n[How self calls this?]", "Come si chiama questo?"),
    ("Could you speak a bit louder?\n[Can-thou speak a bit more strong?]", "Puoi parlare un po' più forte?"),
    ("My Italian is not very good\n[The my Italian not is very good]", "Il mio italiano non è molto buono"),
    ("I understand a bit, but I can't speak well\n[I understand a bit, but not I speak well]", "Capisco un po', ma non parlo bene"),
    ("Thanks for your patience\n[Thanks for the patience]", "Grazie per la pazienza"),

    # --- 4. NAVIGATION & DIRECTIONS ---
    ("Where is... ?\n[Where is...?]", "Dov'è...?"),
    ("Where are...?\n[Where are...?]", "Dove sono...?"),
    ("Where is the bathroom?\n[Where is the bath?]", "Dov'è il bagno?"),
    ("Where is the station?\n[Where is the station?]", "Dov'è la stazione?"),
    ("Where is the bus stop?\n[Where is the stop of the bus?]", "Dov'è la fermata dell'autobus?"),
    ("To the right\n[At right]", "A destra"),
    ("To the left\n[At left]", "A sinistra"),
    ("Straight ahead\n[Straight]", "Dritto"),
    ("Straight on / Keep going straight\n[Always straight]", "Sempre dritto"),
    ("At the corner\n[At the corner]", "All'angolo"),
    ("Near\n[Near]", "Vicino"),
    ("Far\n[Far]", "Lontano"),
    ("Here\n[Here]", "Qui"),
    ("There\n[There / There]", "Lì / Là"),
    ("Opposite / Facing\n[Of front to]", "Di fronte a"),
    ("Next to\n[Alongside to]", "Accanto a"),
    ("How do I get to...?\n[How arrive-I to...?]", "Come arrivo a...?"),
    ("Is it nearby?\n[Is near?]", "È vicino?"),
    ("Is it far from here?\n[Is far from here?]", "È lontano da qui?"),
    ("I am lost\n[Myself I am lost]", "Mi sono perso / persa"),
    ("Where is the entrance?\n[Where is the entry?]", "Dov'è l'ingresso?"),
    ("Where is the exit?\n[Where is the exit?]", "Dov'è l'uscita?"),
    ("Cross the street\n[Cross the street]", "Attraversa la strada"),
    ("Turn right at the traffic light\n[Turn at right at the traffic-light]", "Gira a destra al semaforo"),
    ("Take the first street on the left\n[Take the first street at left]", "Prendi la prima strada a sinistra"),
    ("Behind the building\n[Behind the building]", "Dietro l'edificio"),
    ("In front of the church\n[Before at the church]", "Davanti alla chiesa"),
    ("Between the two shops\n[Between the two shops]", "Tra i due negozi"),
    ("How many minutes on foot?\n[How many minutes at feet?]", "Quanti minuti a piedi?"),
    ("Is it safe to walk here?\n[Is safe to walk here?]", "È sicuro camminare qui?"),

    # --- 5. TRAVEL, TRANSPORT & TICKETS ---
    ("Which platform?\n[Which track?]", "Quale binario?"),
    ("A ticket to..., please\n[A ticket for..., for favor]", "Un biglietto per..., per favore"),
    ("One way or round trip?\n[Only going or return?]", "Solo andata o ritorno?"),
    ("When does the train leave?\n[When departs the train?]", "Quando parte il treno?"),
    ("When does the bus arrive?\n[When arrives the bus?]", "Quando arriva l'autobus?"),
    ("Is this seat free?\n[Is free this seat?]", "È libero questo posto?"),
    ("Where can I validate my ticket?\n[Where can-I to-validate the ticket?]", "Dove posso convalidare il biglietto?"),
    ("Is there a delay?\n[There is a delay?]", "C'è un ritardo?"),
    ("Which bus goes to the center?\n[Which bus goes in center?]", "Quale autobus va in centro?"),
    ("Where do I get off?\n[Where must-I to-descend?]", "Dove devo scendere?"),
    ("I need a taxi\n[I have need of a taxi]", "Ho bisogno di un taxi"),
    ("Please take me to this address\n[Me carry-You to this address, for favor]", "Mi porti a questo indirizzo, per favore"),
    ("How much to go to the airport?\n[How much costs to go to the airport?]", "Quanto costa andare all'aeroporto?"),
    ("Stop here, please\n[Yourself stop-You here, for favor]", "Si fermi qui, per favore"),
    ("Where is the baggage claim?\n[Where is the withdrawal bags?]", "Dov'è il ritiro bagagli?"),
    ("My luggage is lost\n[The my baggage is lost]", "Il mio bagaglio è smarrito"),
    ("I need to rent a car\n[Must-I to-rent a car]", "Devo noleggiare un'auto"),
    ("Where can I park?\n[Where can-I to-park?]", "Dove posso parcheggiare?"),
    ("Is parking free?\n[The parking is free?]", "Il parcheggio è gratuito?"),
    ("Does this train stop in...?\n[This train stops in...?]", "Questo treno ferma a...?"),

    # --- 6. DINING & DRINKING ---
    ("A table for two, please\n[A table for two, for favor]", "Un tavolo per due, per favore"),
    ("Can I see the menu?\n[Can-I to-see the menu?]", "Posso vedere il menu?"),
    ("I would like to order\n[I would wish to order]", "Vorrei ordinare"),
    ("I would like...\n[I would wish...]", "Vorrei..."),
    ("I'll have...\n[I take...]", "Prendo..."),
    ("What do you recommend?\n[What thing to us recommend-You?]", "Che cosa ci consiglia?"),
    ("What is the dish of the day?\n[Which is the dish of the day?]", "Qual è il piatto del giorno?"),
    ("An espresso, please\n[A coffee, for favor]", "Un caffè, per favore"),
    ("A cappuccino, please\n[A cappuccino, for favor]", "Un cappuccio, per favore"),
    ("A glass of water, please\n[A glass of water, for favor]", "Un bicchiere d'acqua, per favore"),
    ("Still or sparkling water?\n[Water natural or sparkling?]", "Acqua naturale o frizzante?"),
    ("House wine\n[Wine of the house]", "Vino della casa"),
    ("A beer, please\n[A beer, for favor]", "Una birra, per favore"),
    ("The bill, please\n[The account, for favor]", "Il conto, per favore"),
    ("Can I pay by card?\n[Can-I to-pay with the card?]", "Posso pagare con la carta?"),
    ("Do you accept credit cards?\n[Accept-you cards of credit?]", "Accettate carte di credito?"),
    ("In cash\n[In cash-money]", "In contanti"),
    ("It's my treat / I'm paying\n[Offer I]", "Offro io"),
    ("Keep the change\n[Keep-You the remainder]", "Tenga il resto"),
    ("It’s delicious!\n[It is delicious!]", "È delizioso!"),
    ("It is very good\n[It is very good]", "È molto buono"),
    ("I am vegetarian\n[I am vegetarian]", "Sono vegetariano/a"),
    ("I am vegan\n[I am vegan]", "Sono vegano/a"),
    ("I am allergic to...\n[I am allergic to...]", "Sono allergico/a a..."),
    ("Gluten-free\n[Without gluten]", "Senza glutine"),
    ("Cheers!\n[Health!]", "Salute!"),
    ("Enjoy your meal!\n[Good appetite!]", "Buon appetito!"),
    ("That's enough, thank you\n[Enough like this, thanks]", "Basta così, grazie"),
    ("Where is the rest room?\n[Where is the toilet?]", "Dov'è la toilette?"),
    ("Can we have split bills?\n[Can-we to-have two accounts separated?]", "Possiamo avere due conti separati?"),
    ("A glass of red / white wine\n[A glass of wine red / white]", "Un bicchiere di vino rosso / bianco"),
    ("Without ice, please\n[Without ice, for favor]", "Senza ghiaccio, per favore"),
    ("Could we have some bread?\n[Can-we to-have of the bread?]", "Possiamo avere del pane?"),
    ("Is service included?\n[The service is included?]", "Il servizio è incluso?"),
    ("I didn't order this\n[Not I have ordered this]", "Non ho ordinato questo"),
    ("Is it spicy?\n[Is spicy?]", "È piccante?"),
    ("Another one, please\n[An other, for favor]", "Un altro, per favore"),
    ("Can I have a receipt?\n[Can-I to-have the receipt?]", "Posso avere la ricevuta?"),
    ("Is there a cover charge?\n[There is the cover-charge?]", "C'è il coperto?"),
    ("To go / Takeaway\n[From transport]", "Da asporto"),

    # --- 7. SHOPPING & MONEY ---
    ("How much does it cost?\n[How much costs?]", "Quanto costa?"),
    ("How much do these cost?\n[How much cost-they?]", "Quanto costano?"),
    ("It is too expensive\n[It is too dear]", "È troppo caro"),
    ("Is there a discount?\n[There is a discount?]", "C'è uno sconto?"),
    ("I'm just looking, thank you\n[I stay only looking, thanks]", "Sto solo guardando, grazie"),
    ("Can I try it on?\n[Can-I to-try-it?]", "Posso provarlo?"),
    ("Where is the fitting room?\n[Where is the dressing-room?]", "Dov'è il camerino?"),
    ("Do you have a larger / smaller size?\n[Have-You a size more big / small?]", "Ha una taglia più grande / piccola?"),
    ("I'll take it\n[It I take]", "Lo prendo"),
    ("I don't want it\n[Not it I want]", "Non lo voglio"),
    ("Do you have...?\n[Have-you...?]", "Avete...?"),
    ("What time do you close?\n[At what hour close-you?]", "A che ora chiudete?"),
    ("What time do you open?\n[At what hour open-you?]", "A che ora aprite?"),
    ("Is it open?\n[Is open?]", "È aperto?"),
    ("Is it closed?\n[Is closed?]", "È chiuso?"),
    ("Where is the ATM?\n[Where is the bank-machine?]", "Dov'è il bancomat?"),
    ("Receipt, please\n[Receipt, for favor]", "Scontrino, per favore"),
    ("Can I have a bag?\n[Can-I to-have a bag?]", "Posso avere un sacchetto?"),
    ("Do you have my size?\n[Have-you the my size?]", "Avete la mia taglia?"),
    ("What brand is it?\n[What brand is?]", "Che marca è?"),
    ("Can we pay separately?\n[Can-we to-pay separately?]", "Possiamo pagare separatamente?"),
    ("Do you have change?\n[Have-you the remainder?]", "Avete il resto?"),
    ("Is it on sale?\n[Is in sale/discount?]", "È in saldo?"),
    ("Where can I buy...?\n[Where can-I to-buy...?]", "Dove posso comprare...?"),
    ("It's good quality\n[It is of good quality]", "È di buona qualità"),
    ("I'm looking for...\n[I stay searching...]", "Sto cercando..."),
    ("Can I pay with contactless?\n[Can-I to-pay contactless?]", "Posso pagare contactless?"),
    ("Do you have another color?\n[Of it have-you an other color?]", "Ne avete un altro colore?"),
    ("Can I exchange this?\n[Can-I to-change-it?]", "Posso cambiarlo?"),
    ("I'd like a refund\n[I would wish a refund]", "Vorrei un rimborso"),

    # --- 8. ACCOMMODATIONS & HOTELS ---
    ("I have a reservation\n[I have a reservation]", "Ho una prenotazione"),
    ("Under the name...\n[At name of...]", "A nome di..."),
    ("Do you have a vacant room?\n[Have-you a room free?]", "Avete una camera libera?"),
    ("For how many nights?\n[For how-many nights?]", "Per quante notti?"),
    ("For one night / two nights\n[For one night / two nights]", "Per una notte / due notti"),
    ("Single / Double room\n[Room single / double]", "Camera singola / doppia"),
    ("With a double bed\n[With bed matrimonial]", "Con letto matrimoniale"),
    ("Is breakfast included?\n[The breakfast is included?]", "La colazione è inclusa?"),
    ("What time is check-out?\n[At what hour is the check-out?]", "A che ora è il check-out?"),
    ("Can I leave my luggage here?\n[Can-I to-leave the baggages here?]", "Posso lasciare i bagagli qui?"),
    ("The key, please\n[The key, for favor]", "La chiave, per favore"),
    ("The air conditioning doesn't work\n[The air conditioned not works]", "L'aria condizionata non funziona"),
    ("There is no hot water\n[Not there is water hot]", "Non c'è acqua calda"),
    ("What is the Wi-Fi password?\n[Which is the password of the Wi-Fi?]", "Qual è la password del Wi-Fi?"),
    ("Could I have an extra towel?\n[Can-I to-have a towel in more?]", "Posso avere un asciugamano in più?"),
    ("Where is the elevator?\n[Where is the elevator?]", "Dov'è l'ascensore?"),
    ("It's very noisy\n[It is very noisy]", "È molto rumoroso"),
    ("Can you wake me up at 7?\n[Can-You wake-me at seven?]", "Può svegliarmi alle sette?"),
    ("Is there a safe in the room?\n[There is a safe-box in room?]", "C'è una cassaforte in camera?"),
    ("I had a great stay\n[Myself I found very-well]", "Mi sono trovato/a benissimo"),

    # --- 9. TIME, DATES & WEATHER ---
    ("What time is it?\n[What hour is?]", "Che ora è?"),
    ("It is one o'clock\n[It is the one]", "È l'una"),
    ("It is two / three / four o'clock\n[They are the two / three / four]", "Sono le due / tre / quattro"),
    ("Today\n[Today]", "Oggi"),
    ("Tomorrow\n[Tomorrow]", "Domani"),
    ("Yesterday\n[Yesterday]", "Ieri"),
    ("Tonight / This evening\n[This-evening]", "Stasera"),
    ("This morning\n[This-morning]", "Stamattina"),
    ("Afternoon\n[After-noon]", "Pomeriggio"),
    ("Now\n[Now]", "Adesso"),
    ("Later\n[More late]", "Più tardi"),
    ("Before\n[Before]", "Prima"),
    ("After\n[After]", "Dopo"),
    ("Early / Soon\n[Early]", "Presto"),
    ("Late\n[Late]", "Tardi"),
    ("The weekend\n[The end week]", "Il fine settimana"),
    ("What day is today?\n[What day is today?]", "Che giorno è oggi?"),
    ("At what time?\n[At what hour?]", "A che ora?"),
    ("In a short while\n[Between little]", "Tra poco"),
    ("Always / Never\n[Always / Never]", "Sempre / Mai"),
    ("See you tomorrow\n[To tomorrow]", "A domani"),
    ("Yesterday evening\n[Yesterday evening]", "Ieri sera"),
    ("Next week\n[The week next]", "La settimana prossima"),
    ("Last week\n[The week last]", "La settimana scorsa"),
    ("What's the weather like?\n[What weather makes-it?]", "Che tempo fa?"),
    ("It's nice weather\n[It makes beautiful weather]", "Fa bel tempo"),
    ("It's cold / hot\n[It makes cold / hot]", "Fa freddo / caldo"),
    ("It's raining\n[It stays raining]", "Sta piovendo"),
    ("It's sunny\n[There is the sun]", "C'è il sole"),
    ("It's windy\n[There is wind]", "C'è vento"),

    # --- 10. EMERGENCIES, MEDICAL & SAFETY ---
    ("Help!\n[Help!]", "Aiuto!"),
    ("Call the police!\n[Call-You the police!]", "Chiami la polizia!"),
    ("Call an ambulance!\n[Call-You an ambulance!]", "Chiami un'ambulanza!"),
    ("I need a doctor\n[I have need of a doctor]", "Ho bisogno di un medico"),
    ("Where is the hospital?\n[Where is the hospital?]", "Dov'è l'ospedale?"),
    ("Where is the pharmacy?\n[Where is the pharmacy?]", "Dov'è la farmacia?"),
    ("I feel sick\n[Myself I feel ill]", "Mi sento male"),
    ("I have pain here\n[I have pain here]", "Ho dolore qui"),
    ("Watch out! / Be careful!\n[Attentive!]", "Attento! / Attenta!"),
    ("I lost my passport\n[I have lost the my passport]", "Ho perso il mio passaporto"),
    ("I lost my phone\n[I have lost the phone]", "Ho perso il telefono"),
    ("There has been an accident\n[There has been an accident]", "C'è stato un incidente"),
    ("Emergency\n[Emergency]", "Emergenza"),
    ("I am unwell\n[I stay ill]", "Sto male"),
    ("Go away!\n[Go away!]", "Vai via!"),
    ("I was robbed\n[I was robbed]", "Sono stato/a derubato/a"),
    ("Where is the police station?\n[Where is the police-station?]", "Dov'è la questura?"),
    ("I have a fever\n[I have the fever]", "Ho la febbre"),
    ("I need medicine for...\n[I have need of a medicine for...]", "Ho bisogno di una medicina per..."),
    ("I am allergic to penicillin\n[I am allergic to-the penicillin]", "Sono allergico/a alla penicillina"),
    ("My head hurts\n[To-me makes pain the head]", "Mi fa male la testa"),
    ("My stomach hurts\n[To-me makes pain the stomach]", "Mi fa male lo stomaco"),
    ("Call a doctor, please\n[Call-You a doctor, for favor]", "Chiami un medico, per favore"),
    ("Stop, thief!\n[To-the thief!]", "Al ladro!"),
    ("I lost my wallet\n[I have lost the wallet]", "Ho perso il portafoglio"),

    # --- 11. TECHNOLOGY & PHONES ---
    ("Is there Wi-Fi here?\n[There is the Wi-Fi here?]", "C'è il Wi-Fi qui?"),
    ("Can I charge my phone here?\n[Can-I to-charge the phone here?]", "Posso caricare il telefono qui?"),
    ("Do you have a phone charger?\n[Hast-thou a battery-charger?]", "Hai un caricabatterie?"),
    ("Where can I buy a SIM card?\n[Where can-I to-buy a SIM?]", "Dove posso comprare una SIM?"),
    ("There is no signal\n[Not there is field]", "Non c'è campo"),
    ("My phone is dead\n[The my phone is discharged]", "Il mio telefono è scarico"),
    ("What is the phone number?\n[Which is the number of phone?]", "Qual è il numero di telefono?"),
    ("Can I take a picture?\n[Can-I to-make a photo?]", "Posso fare una photo?"),
    ("Would you take a picture of us?\n[To-us makes-You a photo, for favor?]", "Ci fa una foto, per favore?"),
    ("Send me a message\n[Send-me a message]", "Mandami un messaggio"),

    # --- 12. EXPRESSING OPINIONS, FEELINGS & NEEDS ---
    ("I like it\n[To-me it pleases]", "Mi piace"),
    ("I don't like it\n[Not to-me it pleases]", "Non mi piace"),
    ("I love it!\n[It I adore! / To-me it pleases very-much!]", "Lo adoro! / Mi piace tantissimo!"),
    ("I agree\n[I am of agreement]", "Sono d'accordo"),
    ("I disagree\n[Not I am of agreement]", "Non sono d'accordo"),
    ("I think that...\n[I think that...]", "Penso che..."),
    ("In my opinion\n[According to me]", "Secondo me"),
    ("I need...\n[I have need of...]", "Ho bisogno di..."),
    ("I want...\n[I want...]", "Voglio..."),
    ("I don't care\n[Not to-me of-it matters]", "Non me ne importa"),
    ("I'm tired\n[I am tired]", "Sono stanco/a"),
    ("I'm hungry\n[I have hunger]", "Ho fame"),
    ("I'm thirsty\n[I have thirst]", "Ho sete"),
    ("I'm cold / hot\n[I have cold / heat]", "Ho freddo / caldo"),
    ("I'm sleepy\n[I have sleepiness]", "Ho sonno"),
    ("I'm busy\n[I am occupied]", "Sono occupato/a"),
    ("I'm ready\n[I am ready]", "Sono pronto/a"),
    ("I am happy\n[I am happy]", "Sono contento/a"),
    ("I am sad\n[I am sad]", "Sono triste"),
    ("Don't worry\n[Not thyself worry-thou / Not Yourself worry-You]", "Non ti preoccupare / Non si preoccupi"),

    # --- 13. IDIOMS, SLANG & EXPRESSIONS ---
    ("How wonderful!\n[What beautiful!]", "Che bello!"),
    ("What a pity! / What a shame!\n[What sin/pity!]", "Che peccato!"),
    ("Oh my goodness!\n[My mama!]", "Mamma mia!"),
    ("Good luck!\n[Into mouth of-the wolf!]", "In bocca al lupo!"),
    ("Response to 'In bocca al lupo'\n[May-he die, the wolf!]", "Crepi il lupo!"),
    ("Makes sense / Sounds good\n[There it stays]", "Ci sta"),
    ("Thank goodness!\n[Less bad!]", "Meno male!"),
    ("I wish! / If only!\n[Maybe! / If only!]", "Magari!"),
    ("Come on! / Stop it!\n[Give!]", "Dai!"),
    ("I don't know / Beats me!\n[(Sound of indifference)]", "Boh!"),
    ("I can't wait\n[Not I see the hour]", "Non vedo l'ora"),
    ("To be in a bad mood\n[To have the moon crooked]", "Avere la luna storta"),
    ("To kill two birds with one stone\n[To take two pigeons with one fava-bean]", "Prendere due piccioni con una fava"),
    ("The sweetness of doing nothing\n[The sweet doing nothing]", "La dolce far niente"),
    ("What a mess!\n[What casino/mess!]", "Che casino!"),
    ("Are you kidding?\n[But art-thou joking?]", "Ma stai scherzando?"),
    ("Whatever! / Forget it!\n[Leave to lose!]", "Lascia perdere!"),
    ("Exactly!\n[Exact!]", "Esatto!"),
    ("Fingers crossed!\n[We cross the fingers!]", "Incrociamo le dita!"),
    ("To cost an arm and a leg\n[To cost an eye of-the head]", "Costare un occhio della testa"),
    ("To hit the nail on the head\n[To hit in-the mark]", "Colpire nel segno"),
    ("It's not a big deal\n[Not it is the end of-the world]", "Non è la fine del mondo"),
    ("Out of the blue\n[At the sudden]", "All'improvviso"),
    ("Speak of the devil\n[Speak-thou of-the devil and sprout-they the horns]", "Parli del diavolo e spuntano le corna"),
    ("I'm exhausted / dead tired\n[I am destroyed]", "Sono distrutto/a")
]

italian_set = dict(ITALIAN_PHRASES)

def app():
    # Inject CSS override to allow newlines (\n) inside Streamlit buttons
    st.markdown("""
    <style>
    .big-font { font-size: 20px !important; text-align: center; }
    .stButton button { height: auto !important; min-height: 60px; width: 100%; font-size: 15px; white-space: pre-wrap !important; word-wrap: break-word; padding: 0.4rem 0.5rem !important; line-height: 1.2 !important; }
    .stButton button div p { white-space: pre-wrap !important; line-height: 1.2 !important; }
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
            
            # Normalize text for display (convert <br> to actual line breaks \n)
            clean_card = card.replace("<br>", "\n").replace(" <br>", "\n")

            with col:
                if idx in st.session_state.matched:
                    team = st.session_state.matched_by_team.get(idx, 0)
                    color = team_colors[team]
                    html_formatted = clean_card.replace("\n", "<br>")
                    st.markdown(f"<div class='big-font card-matched' style='color:{color}'>{html_formatted}</div>", unsafe_allow_html=True)
                else:
                    if st.button(clean_card, key=f"card-{idx}"):
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
            formatted_eng = eng.replace("\n", " ").replace("<br>", " ")
            st.markdown(
                f"**{idx}.** {formatted_eng} ↔️ **{ita}** "
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
