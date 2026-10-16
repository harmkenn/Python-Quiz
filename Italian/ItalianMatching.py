import streamlit as st
import random

# --- Page Setup ---
if __name__ == "__main__":
    st.set_page_config(page_title="Italian Match", layout="wide")

# --- Load custom phrase set: (English + Lit, Italian + Phonetic) ---
ITALIAN_PHRASES = [
    # --- 1. BASIC GREETINGS & FORMALITIES ---
    ("Hi / Bye", "Ciao\n[CHOW]"),
    ("Good morning / Good day\n[Good day]", "Buongiorno\n[bwon-JOHR-noh]"),
    ("Good evening\n[Good evening]", "Buonasera\n[bwon-ah-SEH-rah]"),
    ("Good night\n[Good night]", "Buonanotte\n[bwon-ah-NOHT-teh]"),
    ("Hello (polite / neutral)\n[Safe/Healthy]", "Salve\n[SAHL-veh]"),
    ("Goodbye\n[Until seeing each other again]", "Arrivederci\n[ahr-ree-veh-DEHR-chee]"),
    ("See you soon\n[To soon]", "A presto\n[ah PREHS-toh]"),
    ("See you later\n[To after]", "A dopo\n[ah DOH-poh]"),
    ("See you\n[Us we see]", "Ci vediamo\n[chee veh-DYAH-moh]"),
    ("Please\n[For favor]", "Per favore\n[pehr fah-VOH-reh]"),
    ("Thank you\n[Graces/Thanks]", "Grazie\n[GRAHT-syeh]"),
    ("Thank you very much\n[Thousand thanks]", "Grazie mille\n[GRAHT-syeh MEEL-leh]"),
    ("You're welcome\n[I pray/ask]", "Prego\n[PREH-goh]"),
    ("It's nothing / Don't mention it\n[Of nothing]", "Di niente\n[dee NYEHN-teh]"),
    ("Excuse me (formal)\n[Excuse (you)]", "Scusi\n[SKOO-zee]"),
    ("Excuse me / Sorry\n[Excuse (thou)]", "Scusa\n[SKOO-zah]"),
    ("Excuse me (to pass through)\n[Permission]", "Permesso\n[pehr-MEHS-soh]"),
    ("I'm sorry\n[To me it displeases]", "Mi dispiace\n[mee dees-PYAH-cheh]"),
    ("Yes", "Sì\n[SEE]"),
    ("No", "No\n[NOH]"),
    ("All right / OK\n[It goes well]", "Va bene\n[vah BEH-neh]"),
    ("Pleased to meet you\n[Pleasure]", "Piacere\n[pyah-CHEH-reh]"),
    ("Welcome\n[Well come]", "Benvenuto\n[behn-veh-NOO-toh]"),
    ("Have a good day\n[Good day-duration]", "Buona giornata\n[BWOH-nah johr-NAH-tah]"),
    ("Have a good evening\n[Good evening-duration]", "Buona serata\n[BWOH-nah seh-RAH-tah]"),
    ("Have a good trip\n[Good voyage]", "Buon viaggio\n[bwon VYAHD-joh]"),
    ("Have a good weekend\n[Good end week]", "Buon fine settimana\n[bwon FEE-neh seht-tee-MAH-nah]"),
    ("Have fun!\n[Good fun!]", "Buon divertimento!\n[bwon dee-vehr-tee-MEHN-toh]"),
    ("Happy birthday!\n[Good birthday!]", "Buon compleanno!\n[bwon kohm-pleh-AHN-noh]"),
    ("Congratulations!\n[Congratulations!]", "Congratulazioni!\n[kohn-grah-too-laht-SYOH-nee]"),

    # --- 2. GETTING TO KNOW SOMEONE & SMALL TALK ---
    ("How are you? (formal)\n[How stay (you)]", "Come sta?\n[KOH-meh STAH]"),
    ("How are you? (informal)\n[How stay (thou)]", "Come stai?\n[KOH-meh STHYE]"),
    ("How's it going?\n[How goes?]", "Come va?\n[KOH-meh VAH]"),
    ("I'm doing well, thank you\n[I stay well, thanks]", "Sto bene, grazie\n[stoh BEH-neh, GRAHT-syeh]"),
    ("And you? (formal)\n[And You?]", "E Lei?\n[eh LAY]"),
    ("And you? (informal)\n[And thou?]", "E tu?\n[eh TOO]"),
    ("What is your name? (informal)\n[How yourself call-you?]", "Come ti chiami?\n[KOH-meh tee KYAH-mee]"),
    ("What is your name? (formal)\n[How yourself call-You?]", "Come si chiama?\n[KOH-meh see KYAH-mah]"),
    ("My name is...\n[Myself I call...]", "Mi chiamo...\n[mee KYAH-moh]"),
    ("Where are you from? (informal)\n[Of where art-thou?]", "Di dove sei?\n[dee DOH-veh SAY]"),
    ("Where are you from? (formal)\n[Of where is-You?]", "Di dov'è?\n[dee doh-VEH]"),
    ("I am from...\n[I am of...]", "Sono di...\n[SOH-noh dee]"),
    ("How old are you?\n[How many years have-thou?]", "Quanti anni hai?\n[KWAHN-tee AHN-nee EYE]"),
    ("I am ... years old\n[I have ... years]", "Ho ... anni\n[OH ... AHN-nee]"),
    ("What do you do for a living?\n[What do-thou in the life?]", "Cosa fai nella vita?\n[KOH-zah FYE NEHL-lah VEE-tah]"),
    ("What's up?\n[What self says?]", "Cosa si dice?\n[KOH-zah see DEE-cheh]"),
    ("Everything is good\n[All well]", "Tutto bene\n[TOOT-toh BEH-neh]"),
    ("Not bad\n[Not there is bad]", "Non c'è male\n[nohn cheh MAH-leh]"),
    ("So-so\n[Like this like this]", "Così così\n[koh-ZEE koh-ZEE]"),
    ("Where do you live?\n[Where live-thou?]", "Dove abiti?\n[DOH-veh AH-bee-tee]"),
    ("I live in...\n[I live at...]", "Abito a...\n[AH-bee-toh ah]"),
    ("Are you here on vacation?\n[Art-thou here in vacation?]", "Sei qui in vacanza?\n[SAY kwee een vah-KAHN-tsah]"),
    ("I am here for work\n[I am here for work]", "Sono qui per lavoro\n[SOH-noh kwee pehr lah-VOH-roh]"),
    ("Do you have family here?\n[Hast-thou family here?]", "Hai famiglia qui?\n[EYE fah-MEEL-yah kwee]"),
    ("I am traveling alone\n[I stay traveling from alone]", "Sto viaggiando da solo/a\n[stoh vyahd-JAHN-doh dah SOH-loh/lah]"),
    ("Who are you with?\n[With whom art-thou?]", "Con chi sei?\n[kohn KEE SAY]"),
    ("I am here with my family\n[I am here with the my family]", "Sono qui con la mia famiglia\n[SOH-noh kwee kohn lah MEE-ah fah-MEEL-yah]"),
    ("I am here with friends\n[I am here with of the friends]", "Sono qui con degli amici\n[SOH-noh kwee kohn DEHL-yee ah-MEE-chee]"),
    ("Nice to talk to you\n[It was a pleasure to talk with thee]", "È stato un piacere parlare con te\n[eh STAH-toh oon pyah-CHEH-reh pahr-LAH-reh kohn TEH]"),
    ("Let's keep in touch\n[Hold ourselves in contact]", "Teniamoci in contatto\n[teh-NYAH-moh-chee een kohn-TAHT-toh]"),

    # --- 3. LANGUAGE & COMMUNICATION ---
    ("Do you speak English? (informal)\n[Speak-thou English?]", "Parli inglese?\n[PAHR-lee een-GLEH-zeh]"),
    ("Do you speak English? (formal)\n[Speaks-You English?]", "Parla inglese?\n[PAHR-lah een-GLEH-zeh]"),
    ("I speak a little Italian\n[I speak a little of Italian]", "Parlo un po' di italiano\n[PAHR-loh oon POH dee ee-tahl-YAH-noh]"),
    ("I don't speak Italian\n[Not I speak Italian]", "Non parlo italiano\n[nohn PAHR-loh ee-tahl-YAH-noh]"),
    ("I don't understand\n[Not I understand]", "Non capisco\n[nohn kah-PEES-koh]"),
    ("I understand\n[I understand]", "Capisco\n[kah-PEES-koh]"),
    ("Can you speak more slowly?\n[Can-You speak more slowly?]", "Può parlare più lentamente?\n[pwoh pahr-LAH-reh pyoo lehn-tah-MEHN-teh]"),
    ("Can you repeat that?\n[Can-thou repeat?]", "Puoi ripetere?\n[pwohy ree-PEH-teh-reh]"),
    ("How do you say ... in Italian?\n[How self says ... in Italian?]", "Come si dice ... in italiano?\n[KOH-meh see DEE-cheh ... een ee-tahl-YAH-noh]"),
    ("What does that mean?\n[What thing signifies?]", "Che cosa significa?\n[keh KOH-zah see-NYEE-fee-kah]"),
    ("Could you write it down, please?\n[Can-You write it, for favor?]", "Può scriverlo, per favore?\n[pwoh SKREE-vehr-loh, pehr fah-VOH-reh]"),
    ("How do you spell it?\n[How self writes?]", "Come si scrive?\n[KOH-meh see SKREE-veh]"),
    ("I am learning Italian\n[I stay learning the Italian]", "Sto imparando l'italiano\n[stoh eem-pah-RAHN-doh leet-ahl-YAH-noh]"),
    ("I got it / I understood\n[I have understood]", "Ho capito\n[oh kah-PEE-toh]"),
    ("I didn't get it\n[Not I have understood]", "Non ho capito\n[nohn oh kah-PEE-toh]"),
    ("Can you help me? (formal)\n[Can-You help me?]", "Può aiutarmi?\n[pwoh eye-oo-TAHR-mee]"),
    ("Can you help me? (informal)\n[Can-thou help me?]", "Puoi aiutarmi?\n[pwohy eye-oo-TAHR-mee]"),
    ("What did you say? (formal)\n[What has-You said?]", "Cosa ha detto?\n[KOH-zah ah DEHT-toh]"),
    ("What did you say? (informal)\n[What hast-thou said?]", "Cosa hai detto?\n[KOH-zah eye DEHT-toh]"),
    ("I have a question\n[I have a question]", "Ho una domanda\n[oh OO-nah doh-MAHN-dah]"),
    ("No problem\n[No problem]", "Nessun problema\n[nehs-SOON prohb-LEH-mah]"),
    ("It doesn't matter / Never mind\n[Not imports]", "Non importa\n[nohn eem-POHR-tah]"),
    ("I don't know\n[Not it I know]", "Non lo so\n[nohn loh SOH]"),
    ("I am sure of it\n[Of it I am sure]", "Ne sono sicuro/a\n[neh SOH-noh see-KOO-roh/rah]"),
    ("Are you sure?\n[Art-thou sure?]", "Sei sicuro/a?\n[SAY see-KOO-roh/rah]"),
    ("What is this called?\n[How self calls this?]", "Come si chiama questo?\n[KOH-meh see KYAH-mah KWEHS-toh]"),
    ("Could you speak a bit louder?\n[Can-thou speak a bit more strong?]", "Puoi parlare un po' più forte?\n[pwohy pahr-LAH-reh oon POH pyoo FOHR-teh]"),
    ("My Italian is not very good\n[The my Italian not is very good]", "Il mio italiano non è molto buono\n[eel MEE-oh ee-tahl-YAH-noh nohn eh MOHL-toh BWOH-noh]"),
    ("I understand a bit, but I can't speak well\n[I understand a bit, but not I speak well]", "Capisco un po', ma non parlo bene\n[kah-PEES-koh oon POH, mah nohn PAHR-loh BEH-neh]"),
    ("Thanks for your patience\n[Thanks for the patience]", "Grazie per la pazienza\n[GRAHT-syeh pehr lah paht-SYEHN-tsah]"),

    # --- 4. NAVIGATION & DIRECTIONS ---
    ("Where is... ?\n[Where is...?]", "Dov'è...?\n[doh-VEH]"),
    ("Where are...?\n[Where are...?]", "Dove sono...?\n[DOH-veh SOH-noh]"),
    ("Where is the bathroom?\n[Where is the bath?]", "Dov'è il bagno?\n[doh-VEH eel BAHN-yoh]"),
    ("Where is the station?\n[Where is the station?]", "Dov'è la stazione?\n[doh-VEH lah staht-SYOH-neh]"),
    ("Where is the bus stop?\n[Where is the stop of the bus?]", "Dov'è la fermata dell'autobus?\n[doh-VEH lah fehr-MAH-tah dehl-OW-toh-boos]"),
    ("To the right\n[At right]", "A destra\n[ah DEHS-trah]"),
    ("To the left\n[At left]", "A sinistra\n[ah see-NEES-trah]"),
    ("Straight ahead\n[Straight]", "Dritto\n[DREET-toh]"),
    ("Straight on / Keep going straight\n[Always straight]", "Sempre dritto\n[SEHM-preh DREET-toh]"),
    ("At the corner\n[At the corner]", "All'angolo\n[ahl-LAHN-goh-loh]"),
    ("Near\n[Near]", "Vicino\n[vee-CHEE-noh]"),
    ("Far\n[Far]", "Lontano\n[lohn-TAH-noh]"),
    ("Here\n[Here]", "Qui\n[KWEE]"),
    ("There\n[There / There]", "Lì / Là\n[LEE / LAH]"),
    ("Opposite / Facing\n[Of front to]", "Di fronte a\n[dee FROHN-teh ah]"),
    ("Next to\n[Alongside to]", "Accanto a\n[ahk-KAHN-toh ah]"),
    ("How do I get to...?\n[How arrive-I to...?]", "Come arrivo a...?\n[KOH-meh ahr-REE-voh ah]"),
    ("Is it nearby?\n[Is near?]", "È vicino?\n[eh vee-CHEE-noh]"),
    ("Is it far from here?\n[Is far from here?]", "È lontano da qui?\n[eh lohn-TAH-noh dah KWEE]"),
    ("I am lost\n[Myself I am lost]", "Mi sono perso / persa\n[mee SOH-noh PEHR-soh / PEHR-sah]"),
    ("Where is the entrance?\n[Where is the entry?]", "Dov'è l'ingresso?\n[doh-VEH leen-GREHS-soh]"),
    ("Where is the exit?\n[Where is the exit?]", "Dov'è l'uscita?\n[doh-VEH loo-SHEE-tah]"),
    ("Cross the street\n[Cross the street]", "Attraversa la strada\n[aht-trah-VEHR-sah lah STRAH-dah]"),
    ("Turn right at the traffic light\n[Turn at right at the traffic-light]", "Gira a destra al semaforo\n[JEE-rah ah DEHS-trah ahl seh-MAH-foh-roh]"),
    ("Take the first street on the left\n[Take the first street at left]", "Prendi la prima strada a sinistra\n[PREHN-dee lah PREE-mah STRAH-dah ah see-NEES-trah]"),
    ("Behind the building\n[Behind the building]", "Dietro l'edificio\n[DYEH-troh leh-dee-FEE-choh]"),
    ("In front of the church\n[Before at the church]", "Davanti alla chiesa\n[dah-VAHN-tee AHL-lah KYEH-zah]"),
    ("Between the two shops\n[Between the two shops]", "Tra i due negozi\n[trah ee DOO-eh neh-GOH-tsee]"),
    ("How many minutes on foot?\n[How many minutes at feet?]", "Quanti minuti a piedi?\n[KWAHN-tee mee-NOO-tee ah PYEH-dee]"),
    ("Is it safe to walk here?\n[Is safe to walk here?]", "È sicuro camminare qui?\n[eh see-KOO-roh kahm-mee-NAH-reh KWEE]"),

    # --- 5. TRAVEL, TRANSPORT & TICKETS ---
    ("Which platform?\n[Which track?]", "Quale binario?\n[KWAH-leh bee-NAH-ryoh]"),
    ("A ticket to..., please\n[A ticket for..., for favor]", "Un biglietto per..., per favore\n[oon beel-YEHT-toh pehr, pehr fah-VOH-reh]"),
    ("One way or round trip?\n[Only going or return?]", "Solo andata o ritorno?\n[SOH-loh ahn-DAH-tah oh ree-TOHR-noh]"),
    ("When does the train leave?\n[When departs the train?]", "Quando parte il treno?\n[KWAHN-doh PAHR-teh eel TREH-noh]"),
    ("When does the bus arrive?\n[When arrives the bus?]", "Quando arriva l'autobus?\n[KWAHN-doh ahr-REE-vah low-toh-boos]"),
    ("Is this seat free?\n[Is free this seat?]", "È libero questo posto?\n[eh LEE-beh-roh KWEHS-toh POHS-toh]"),
    ("Where can I validate my ticket?\n[Where can-I to-validate the ticket?]", "Dove posso convalidare il biglietto?\n[DOH-veh POHS-soh kohn-vah-lee-DAH-reh eel beel-YEHT-toh]"),
    ("Is there a delay?\n[There is a delay?]", "C'è un ritardo?\n[cheh oon ree-TAHR-doh]"),
    ("Which bus goes to the center?\n[Which bus goes in center?]", "Quale autobus va in centro?\n[KWAH-leh low-toh-boos vah een CHEHN-troh]"),
    ("Where do I get off?\n[Where must-I to-descend?]", "Dove devo scendere?\n[DOH-veh DEH-voh SHEHN-deh-reh]"),
    ("I need a taxi\n[I have need of a taxi]", "Ho bisogno di un taxi\n[oh bee-ZOHN-yoh dee oon TAHK-see]"),
    ("Please take me to this address\n[Me carry-You to this address, for favor]", "Mi porti a questo indirizzo, per favore\n[mee POHR-tee ah KWEHS-toh een-dee-REET-tsoh, pehr fah-VOH-reh]"),
    ("How much to go to the airport?\n[How much costs to go to the airport?]", "Quanto costa andare all'aeroporto?\n[KWAHN-toh KOHS-tah ahn-DAH-reh ahl-lah-eh-roh-POHR-toh]"),
    ("Stop here, please\n[Yourself stop-You here, for favor]", "Si fermi qui, per favore\n[see FEHR-mee kwee, pehr fah-VOH-reh]"),
    ("Where is the baggage claim?\n[Where is the withdrawal bags?]", "Dov'è il ritiro bagagli?\n[doh-VEH eel ree-TEE-roh bah-GAHL-yee]"),
    ("My luggage is lost\n[The my baggage is lost]", "Il mio bagaglio è smarrito\n[eel MEE-oh bah-GAHL-yoh eh smah-RREET-toh]"),
    ("I need to rent a car\n[Must-I to-rent a car]", "Devo noleggiare un'auto\n[DEH-voh noh-lehd-JAH-reh OO-now-toh]"),
    ("Where can I park?\n[Where can-I to-park?]", "Dove posso parcheggiare?\n[DOH-veh POHS-soh pahr-kehd-JAH-reh]"),
    ("Is parking free?\n[The parking is free?]", "Il parcheggio è gratuito?\n[eel pahr-KEHD-joh eh grah-TOO-ee-toh]"),
    ("Does this train stop in...?\n[This train stops in...?]", "Questo treno ferma a...?\n[KWEHS-toh TREH-noh FEHR-mah ah]"),

    # --- 6. DINING & DRINKING ---
    ("A table for two, please\n[A table for two, for favor]", "Un tavolo per due, per favore\n[oon TAH-voh-loh pehr DOO-eh, pehr fah-VOH-reh]"),
    ("Can I see the menu?\n[Can-I to-see the menu?]", "Posso vedere il menu?\n[POHS-soh veh-DEH-reh eel meh-NOO]"),
    ("I would like to order\n[I would wish to order]", "Vorrei ordinare\n[vohr-RAY ohr-dee-NAH-reh]"),
    ("I would like...\n[I would wish...]", "Vorrei...\n[vohr-RAY]"),
    ("I'll have...\n[I take...]", "Prendo...\n[PREHN-doh]"),
    ("What do you recommend?\n[What thing to us recommend-You?]", "Che cosa ci consiglia?\n[keh KOH-zah chee kohn-SEEL-yah]"),
    ("What is the dish of the day?\n[Which is the dish of the day?]", "Qual è il piatto del giorno?\n[kwahl EH eel PYAH-toh dehl JOHR-noh]"),
    ("An espresso, please\n[A coffee, for favor]", "Un caffè, per favore\n[oon kahf-FEH, pehr fah-VOH-reh]"),
    ("A cappuccino, please\n[A cappuccino, for favor]", "Un cappuccio, per favore\n[oon kahp-POOCH-choh, pehr fah-VOH-reh]"),
    ("A glass of water, please\n[A glass of water, for favor]", "Un bicchiere d'acqua, per favore\n[oon bee-KYEH-reh DAHK-wah, pehr fah-VOH-reh]"),
    ("Still or sparkling water?\n[Water natural or sparkling?]", "Acqua naturale o frizzante?\n[AHK-wah nah-too-RAH-leh oh freet-TZAHN-teh]"),
    ("House wine\n[Wine of the house]", "Vino della casa\n[VEE-noh DEHL-lah KAH-zah]"),
    ("A beer, please\n[A beer, for favor]", "Una birra, per favore\n[OO-nah BEER-rah, pehr fah-VOH-reh]"),
    ("The bill, please\n[The account, for favor]", "Il conto, per favore\n[eel KAHN-toh, pehr fah-VOH-reh]"),
    ("Can I pay by card?\n[Can-I to-pay with the card?]", "Posso pagare con la carta?\n[POHS-soh pah-GAH-reh kohn lah KAHR-tah]"),
    ("Do you accept credit cards?\n[Accept-you cards of credit?]", "Accettate carte di credito?\n[ahch-cheht-TAH-teh KAHR-teh dee CREH-dee-toh]"),
    ("In cash\n[In cash-money]", "In contanti\n[een kohn-TAHN-tee]"),
    ("It's my treat / I'm paying\n[Offer I]", "Offro io\n[OHF-froh EE-oh]"),
    ("Keep the change\n[Keep-You the remainder]", "Tenga il resto\n[TEHN-gah eel REHS-toh]"),
    ("It’s delicious!\n[It is delicious!]", "È delizioso!\n[eh deh-leet-SYOH-zoh]"),
    ("It is very good\n[It is very good]", "È molto buono\n[eh MOHL-toh BWOH-noh]"),
    ("I am vegetarian\n[I am vegetarian]", "Sono vegetariano/a\n[SOH-noh veh-jeh-tah-RYAH-noh/nah]"),
    ("I am vegan\n[I am vegan]", "Sono vegano/a\n[SOH-noh veh-GAH-noh/nah]"),
    ("I am allergic to...\n[I am allergic to...]", "Sono allergico/a a...\n[SOH-noh ahl-LEHR-jee-koh/kah ah]"),
    ("Gluten-free\n[Without gluten]", "Senza glutine\n[SEHN-tsah GLOO-tee-neh]"),
    ("Cheers!\n[Health!]", "Salute!\n[sah-LOO-teh]"),
    ("Enjoy your meal!\n[Good appetite!]", "Buon appetito!\n[bwon ahp-peh-TEE-toh]"),
    ("That's enough, thank you\n[Enough like this, thanks]", "Basta così, grazie\n[BAHS-tah koh-ZEE, GRAHT-syeh]"),
    ("Where is the rest room?\n[Where is the toilet?]", "Dov'è la toilette?\n[doh-VEH lah twah-LEHT]"),
    ("Can we have split bills?\n[Can-we to-have two accounts separated?]", "Possiamo avere due conti separati?\n[pohs-SYAH-moh ah-VEH-reh DOO-eh KAHN-tee seh-pah-RAH-tee]"),
    ("A glass of red / white wine\n[A glass of wine red / white]", "Un bicchiere di vino rosso / bianco\n[oon bee-KYEH-reh dee VEE-noh ROHS-soh / BYAHN-koh]"),
    ("Without ice, please\n[Without ice, for favor]", "Senza ghiaccio, per favore\n[SEHN-tsah GYAHCH-choh, pehr fah-VOH-reh]"),
    ("Could we have some bread?\n[Can-we to-have of the bread?]", "Possiamo avere del pane?\n[pohs-SYAH-moh ah-VEH-reh dehl PAH-neh]"),
    ("Is service included?\n[The service is included?]", "Il servizio è incluso?\n[eel sehr-VEET-syoh eh een-KLOO-zoh]"),
    ("I didn't order this\n[Not I have ordered this]", "Non ho ordinato questo\n[nohn oh ohr-dee-NAH-toh KWEHS-toh]"),
    ("Is it spicy?\n[Is spicy?]", "È piccante?\n[eh peek-KAHN-teh]"),
    ("Another one, please\n[An other, for favor]", "Un altro, per favore\n[oon AHL-troh, pehr fah-VOH-reh]"),
    ("Can I have a receipt?\n[Can-I to-have the receipt?]", "Posso avere la ricevuta?\n[POHS-soh ah-VEH-reh lah ree-cheh-VOO-tah]"),
    ("Is there a cover charge?\n[There is the cover-charge?]", "C'è il coperto?\n[cheh eel koh-PEHR-toh]"),
    ("To go / Takeaway\n[From transport]", "Da asporto\n[dah ahs-POHR-toh]"),

    # --- 7. SHOPPING & MONEY ---
    ("How much does it cost?\n[How much costs?]", "Quanto costa?\n[KWAHN-toh KOHS-tah]"),
    ("How much do these cost?\n[How much cost-they?]", "Quanto costano?\n[KWAHN-toh KOHS-tah-noh]"),
    ("It is too expensive\n[It is too dear]", "È troppo caro\n[eh TROHP-poh KAH-roh]"),
    ("Is there a discount?\n[There is a discount?]", "C'è uno sconto?\n[cheh OO-noh SKOHN-toh]"),
    ("I'm just looking, thank you\n[I stay only looking, thanks]", "Sto solo guardando, grazie\n[stoh SOH-loh gwahr-DAHN-doh, GRAHT-syeh]"),
    ("Can I try it on?\n[Can-I to-try-it?]", "Posso provarlo?\n[POHS-soh proh-VAHR-loh]"),
    ("Where is the fitting room?\n[Where is the dressing-room?]", "Dov'è il camerino?\n[doh-VEH eel kah-meh-REE-noh]"),
    ("Do you have a larger / smaller size?\n[Have-You a size more big / small?]", "Ha una taglia più grande / piccola?\n[ah OO-nah TAHL-yah pyoo GRAHN-deh / PEEK-koh-lah]"),
    ("I'll take it\n[It I take]", "Lo prendo\n[loh PREHN-doh]"),
    ("I don't want it\n[Not it I want]", "Non lo voglio\n[nohn loh VOHL-yoh]"),
    ("Do you have...?\n[Have-you...?]", "Avete...?\n[ah-VEH-teh]"),
    ("What time do you close?\n[At what hour close-you?]", "A che ora chiudete?\n[ah keh OH-rah kyoo-DEH-teh]"),
    ("What time do you open?\n[At what hour open-you?]", "A che ora aprite?\n[ah keh OH-rah ah-PREE-teh]"),
    ("Is it open?\n[Is open?]", "È aperto?\n[eh ah-PEHR-toh]"),
    ("Is it closed?\n[Is closed?]", "È chiuso?\n[eh KYOO-zoh]"),
    ("Where is the ATM?\n[Where is the bank-machine?]", "Dov'è il bancomat?\n[doh-VEH eel BAHN-koh-maht]"),
    ("Receipt, please\n[Receipt, for favor]", "Scontrino, per favore\n[skohn-TREE-noh, pehr fah-VOH-reh]"),
    ("Can I have a bag?\n[Can-I to-have a bag?]", "Posso avere un sacchetto?\n[POHS-soh ah-VEH-reh oon sahks-KEHT-toh]"),
    ("Do you have my size?\n[Have-you the my size?]", "Avete la mia taglia?\n[ah-VEH-teh lah MEE-ah TAHL-yah]"),
    ("What brand is it?\n[What brand is?]", "Che marca è?\n[keh MAHR-kah eh]"),
    ("Can we pay separately?\n[Can-we to-pay separately?]", "Possiamo pagare separatamente?\n[pohs-SYAH-moh pah-GAH-reh seh-pah-rah-tah-MEHN-teh]"),
    ("Do you have change?\n[Have-you the remainder?]", "Avete il resto?\n[ah-VEH-teh eel REHS-toh]"),
    ("Is it on sale?\n[Is in sale/discount?]", "È in saldo?\n[eh een SAHL-doh]"),
    ("Where can I buy...?\n[Where can-I to-buy...?]", "Dove posso comprare...?\n[DOH-veh POHS-soh kohm-PRAH-reh]"),
    ("It's good quality\n[It is of good quality]", "È di buona qualità\n[eh dee BWOH-nah kwah-lee-TAH]"),
    ("I'm looking for...\n[I stay searching...]", "Sto cercando...\n[stoh chehr-KAHN-doh]"),
    ("Can I pay with contactless?\n[Can-I to-pay contactless?]", "Posso pagare contactless?\n[POHS-soh pah-GAH-reh kohn-tahkt-lehs]"),
    ("Do you have another color?\n[Of it have-you an other color?]", "Ne avete un altro colore?\n[neh ah-VEH-teh oon AHL-troh koh-LOH-reh]"),
    ("Can I exchange this?\n[Can-I to-change-it?]", "Posso cambiarlo?\n[POHS-soh kahm-BYAHR-loh]"),
    ("I'd like a refund\n[I would wish a refund]", "Vorrei un rimborso\n[vohr-RAY oon reem-BOHR-soh]"),

    # --- 8. ACCOMMODATIONS & HOTELS ---
    ("I have a reservation\n[I have a reservation]", "Ho una prenotazione\n[oh OO-nah preh-noh-taht-SYOH-neh]"),
    ("Under the name...\n[At name of...]", "A nome di...\n[ah NOH-meh dee]"),
    ("Do you have a vacant room?\n[Have-you a room free?]", "Avete una camera libera?\n[ah-VEH-teh OO-nah KAH-meh-rah LEE-beh-rah]"),
    ("For how many nights?\n[For how-many nights?]", "Per quante notti?\n[pehr KWAHN-teh NOHT-tee]"),
    ("For one night / two nights\n[For one night / two nights]", "Per una notte / due notti\n[pehr OO-nah NOHT-teh / DOO-eh NOHT-tee]"),
    ("Single / Double room\n[Room single / double]", "Camera singola / doppia\n[KAH-meh-rah SEEN-goh-lah / DOHP-pyah]"),
    ("With a double bed\n[With bed matrimonial]", "Con letto matrimoniale\n[kohn LEHT-toh mah-tree-moh-NYAH-leh]"),
    ("Is breakfast included?\n[The breakfast is included?]", "La colazione è inclusa?\n[lah koh-laht-SYOH-neh eh een-KLOO-zah]"),
    ("What time is check-out?\n[At what hour is the check-out?]", "A che ora è il check-out?\n[ah keh OH-rah eh eel chehk-owt]"),
    ("Can I leave my luggage here?\n[Can-I to-leave the baggages here?]", "Posso lasciare i bagagli qui?\n[POHS-soh lah-SHAH-reh ee bah-GAHL-yee KWEE]"),
    ("The key, please\n[The key, for favor]", "La chiave, per favore\n[lah KYAH-veh, pehr fah-VOH-reh]"),
    ("The air conditioning doesn't work\n[The air conditioned not works]", "L'aria condizionata non funziona\n[LAH-ryah kohn-dee-tsyoh-NAH-tah nohn foon-TSYOH-nah]"),
    ("There is no hot water\n[Not there is water hot]", "Non c'è acqua calda\n[nohn cheh AHK-wah KAHL-dah]"),
    ("What is the Wi-Fi password?\n[Which is the password of the Wi-Fi?]", "Qual è la password del Wi-Fi?\n[kwahl eh lah pahs-woohrd dehl wee-fee]"),
    ("Could I have an extra towel?\n[Can-I to-have a towel in more?]", "Posso avere un asciugamano in più?\n[POHS-soh ah-VEH-reh oon ah-shoo-gah-MAH-noh een pyoo]"),
    ("Where is the elevator?\n[Where is the elevator?]", "Dov'è l'ascensore?\n[doh-VEH lah-shehn-SOH-reh]"),
    ("It's very noisy\n[It is very noisy]", "È molto rumoroso\n[eh MOHL-toh roo-moh-ROH-zoh]"),
    ("Can you wake me up at 7?\n[Can-You wake-me at seven?]", "Può svegliarmi alle sette?\n[pwoh zvehl-YAHR-mee AHL-leh SEHT-teh]"),
    ("Is there a safe in the room?\n[There is a safe-box in room?]", "C'è una cassaforte in camera?\n[cheh OO-nah kahs-sah-FOHR-teh een KAH-meh-rah]"),
    ("I had a great stay\n[Myself I found very-well]", "Mi sono trovato/a benissimo\n[mee SOH-noh troh-VAH-toh/tah beh-NEES-see-moh]"),

    # --- 9. TIME, DATES & WEATHER ---
    ("What time is it?\n[What hour is?]", "Che ora è?\n[keh OH-rah eh]"),
    ("It is one o'clock\n[It is the one]", "È l'una\n[eh LOO-nah]"),
    ("It is two / three / four o'clock\n[They are the two / three / four]", "Sono le due / tre / quattro\n[SOH-noh leh DOO-eh / TREH / KWAHT-troh]"),
    ("Today\n[Today]", "Oggi\n[OHD-jee]"),
    ("Tomorrow\n[Tomorrow]", "Domani\n[doh-MAH-nee]"),
    ("Yesterday\n[Yesterday]", "Ieri\n[YEH-ree]"),
    ("Tonight / This evening\n[This-evening]", "Stasera\n[stah-SEH-rah]"),
    ("This morning\n[This-morning]", "Stamattina\n[stah-maht-TEE-nah]"),
    ("Afternoon\n[After-noon]", "Pomeriggio\n[poh-meh-REED-joh]"),
    ("Now\n[Now]", "Adesso\n[ah-DEHS-soh]"),
    ("Later\n[More late]", "Più tardi\n[pyoo TAHR-dee]"),
    ("Before\n[Before]", "Prima\n[PREE-mah]"),
    ("After\n[After]", "Dopo\n[DOH-poh]"),
    ("Early / Soon\n[Early]", "Presto\n[PREHS-toh]"),
    ("Late\n[Late]", "Tardi\n[TAHR-dee]"),
    ("The weekend\n[The end week]", "Il fine settimana\n[eel FEE-neh seht-tee-MAH-nah]"),
    ("What day is today?\n[What day is today?]", "Che giorno è oggi?\n[keh JOHR-noh eh OHD-jee]"),
    ("At what time?\n[At what hour?]", "A che ora?\n[ah keh OH-rah]"),
    ("In a short while\n[Between little]", "Tra poco\n[trah POH-koh]"),
    ("Always / Never\n[Always / Never]", "Sempre / Mai\n[SEHM-preh / MYE]"),
    ("See you tomorrow\n[To tomorrow]", "A domani\n[ah doh-MAH-nee]"),
    ("Yesterday evening\n[Yesterday evening]", "Ieri sera\n[YEH-ree SEH-rah]"),
    ("Next week\n[The week next]", "La settimana prossima\n[lah seht-tee-MAH-nah PROHS-see-mah]"),
    ("Last week\n[The week last]", "La settimana scorsa\n[lah seht-tee-MAH-nah SKOHR-sah]"),
    ("What's the weather like?\n[What weather makes-it?]", "Che tempo fa?\n[keh TEHM-poh FAH]"),
    ("It's nice weather\n[It makes beautiful weather]", "Fa bel tempo\n[fah behl TEHM-poh]"),
    ("It's cold / hot\n[It makes cold / hot]", "Fa freddo / caldo\n[fah FREHD-doh / KAHL-doh]"),
    ("It's raining\n[It stays raining]", "Sta piovendo\n[stah pyoh-VEHN-doh]"),
    ("It's sunny\n[There is the sun]", "C'è il sole\n[cheh eel SOH-leh]"),
    ("It's windy\n[There is wind]", "C'è vento\n[cheh VEHN-toh]"),

    # --- 10. EMERGENCIES, MEDICAL & SAFETY ---
    ("Help!\n[Help!]", "Aiuto!\n[ah-YOO-toh]"),
    ("Call the police!\n[Call-You the police!]", "Chiami la polizia!\n[KYAH-mee lah poh-leet-SEE-ah]"),
    ("Call an ambulance!\n[Call-You an ambulance!]", "Chiami un'ambulanza!\n[KYAH-mee oon-ahm-boo-LAHN-tsah]"),
    ("I need a doctor\n[I have need of a doctor]", "Ho bisogno di un medico\n[oh bee-ZOHN-yoh dee oon MEH-dee-koh]"),
    ("Where is the hospital?\n[Where is the hospital?]", "Dov'è l'ospedale?\n[doh-VEH lohs-peh-DAH-leh]"),
    ("Where is the pharmacy?\n[Where is the pharmacy?]", "Dov'è la farmacia?\n[doh-VEH lah fahr-mah-CHEE-ah]"),
    ("I feel sick\n[Myself I feel ill]", "Mi sento male\n[mee SEHN-toh MAH-leh]"),
    ("I have pain here\n[I have pain here]", "Ho dolore qui\n[oh doh-LOH-reh KWEE]"),
    ("Watch out! / Be careful!\n[Attentive!]", "Attento! / Attenta!\n[aht-TEHN-toh / aht-TEHN-tah]"),
    ("I lost my passport\n[I have lost the my passport]", "Ho perso il mio passaporto\n[oh PEHR-soh eel MEE-oh pahs-sah-POHR-toh]"),
    ("I lost my phone\n[I have lost the phone]", "Ho perso il telefono\n[oh PEHR-soh eel teh-LEH-foh-noh]"),
    ("There has been an accident\n[There has been an accident]", "C'è stato un incidente\n[cheh STAH-toh oon een-chee-DEHN-teh]"),
    ("Emergency\n[Emergency]", "Emergenza\n[eh-mehr-JEHN-tsah]"),
    ("I am unwell\n[I stay ill]", "Sto male\n[stoh MAH-leh]"),
    ("Go away!\n[Go away!]", "Vai via!\n[vye VEE-ah]"),
    ("I was robbed\n[I was robbed]", "Sono stato/a derubato/a\n[SOH-noh STAH-toh/tah deh-roo-BAH-toh/tah]"),
    ("Where is the police station?\n[Where is the police-station?]", "Dov'è la questura?\n[doh-VEH lah kwehs-TOO-rah]"),
    ("I have a fever\n[I have the fever]", "Ho la febbre\n[oh lah FEHB-breh]"),
    ("I need medicine for...\n[I have need of a medicine for...]", "Ho bisogno di una medicina per...\n[oh bee-ZOHN-yoh dee OO-nah meh-dee-CHEE-nah pehr]"),
    ("I am allergic to penicillin\n[I am allergic to-the penicillin]", "Sono allergico/a alla penicillina\n[SOH-noh ahl-LEHR-jee-koh/kah AHL-lah peh-nee-cheel-LEE-nah]"),
    ("My head hurts\n[To-me makes pain the head]", "Mi fa male la testa\n[mee fah MAH-leh lah TEHS-tah]"),
    ("My stomach hurts\n[To-me makes pain the stomach]", "Mi fa male lo stomaco\n[mee fah MAH-leh loh STOH-mah-koh]"),
    ("Call a doctor, please\n[Call-You a doctor, for favor]", "Chiami un medico, per favore\n[KYAH-mee oon MEH-dee-koh, pehr fah-VOH-reh]"),
    ("Stop, thief!\n[To-the thief!]", "Al ladro!\n[ahl LAH-droh]"),
    ("I lost my wallet\n[I have lost the wallet]", "Ho perso il portafoglio\n[oh PEHR-soh eel pohr-tah-FOHL-yoh]"),

    # --- 11. TECHNOLOGY & PHONES ---
    ("Is there Wi-Fi here?\n[There is the Wi-Fi here?]", "C'è il Wi-Fi qui?\n[cheh eel wee-fee KWEE]"),
    ("Can I charge my phone here?\n[Can-I to-charge the phone here?]", "Posso caricare il telefono qui?\n[POHS-soh kah-ree-KAH-reh eel teh-LEH-foh-noh KWEE]"),
    ("Do you have a phone charger?\n[Hast-thou a battery-charger?]", "Hai un caricabatterie?\n[EYE oon kah-ree-kah-baht-teh-REE-eh]"),
    ("Where can I buy a SIM card?\n[Where can-I to-buy a SIM?]", "Dove posso comprare una SIM?\n[DOH-veh POHS-soh kohm-PRAH-reh OO-nah SEEM]"),
    ("There is no signal\n[Not there is field]", "Non c'è campo\n[nohn cheh KAHM-poh]"),
    ("My phone is dead\n[The my phone is discharged]", "Il mio telefono è scarico\n[eel MEE-oh teh-LEH-foh-noh eh SKAH-ree-koh]"),
    ("What is the phone number?\n[Which is the number of phone?]", "Qual è il numero di telefono?\n[kwahl eh eel NOO-meh-roh dee teh-LEH-foh-noh]"),
    ("Can I take a picture?\n[Can-I to-make a photo?]", "Posso fare una foto?\n[POHS-soh FAH-reh OO-nah FOH-toh]"),
    ("Would you take a picture of us?\n[To-us makes-You a photo, for favor?]", "Ci fa una foto, per favore?\n[chee fah OO-nah FOH-toh, pehr fah-VOH-reh]"),
    ("Send me a message\n[Send-me a message]", "Mandami un messaggio\n[MAHN-dah-mee oon mehs-SAHD-joh]"),

    # --- 12. EXPRESSING OPINIONS, FEELINGS & NEEDS ---
    ("I like it\n[To-me it pleases]", "Mi piace\n[mee PYAH-cheh]"),
    ("I don't like it\n[Not to-me it pleases]", "Non mi piace\n[nohn mee PYAH-cheh]"),
    ("I love it!\n[It I adore! / To-me it pleases very-much!]", "Lo adoro! / Mi piace tantissimo!\n[loh ah-DOH-roh / mee PYAH-cheh tahn-TEES-see-moh]"),
    ("I agree\n[I am of agreement]", "Sono d'accordo\n[SOH-noh dahk-KOHR-doh]"),
    ("I disagree\n[Not I am of agreement]", "Non sono d'accordo\n[nohn SOH-noh dahk-KOHR-doh]"),
    ("I think that...\n[I think that...]", "Penso che...\n[PEHN-soh keh]"),
    ("In my opinion\n[According to me]", "Secondo me\n[seh-KOHN-doh MEH]"),
    ("I need...\n[I have need of...]", "Ho bisogno di...\n[oh bee-ZOHN-yoh dee]"),
    ("I want...\n[I want...]", "Voglio...\n[VOHL-yoh]"),
    ("I don't care\n[Not to-me of-it matters]", "Non me ne importa\n[nohn meh neh eem-POHR-tah]"),
    ("I'm tired\n[I am tired]", "Sono stanco/a\n[SOH-noh STAHN-koh/kah]"),
    ("I'm hungry\n[I have hunger]", "Ho fame\n[oh FAH-meh]"),
    ("I'm thirsty\n[I have thirst]", "Ho sete\n[oh SEH-teh]"),
    ("I'm cold / hot\n[I have cold / heat]", "Ho freddo / caldo\n[oh FREHD-doh / KAHL-doh]"),
    ("I'm sleepy\n[I have sleepiness]", "Ho sonno\n[oh SOHN-noh]"),
    ("I'm busy\n[I am occupied]", "Sono occupato/a\n[SOH-noh ohk-koo-PAH-toh/tah]"),
    ("I'm ready\n[I am ready]", "Sono pronto/a\n[SOH-noh PROHN-toh/tah]"),
    ("I am happy\n[I am happy]", "Sono contento/a\n[SOH-noh kohn-TEHN-toh/tah]"),
    ("I am sad\n[I am sad]", "Sono triste\n[SOH-noh TREES-teh]"),
    ("Don't worry\n[Not thyself worry-thou / Not Yourself worry-You]", "Non ti preoccupare / Non si preoccupi\n[nohn tee preh-ohk-koo-PAH-reh / nohn see preh-OHK-koo-pee]"),

    # --- 13. IDIOMS, SLANG & EXPRESSIONS ---
    ("How wonderful!\n[What beautiful!]", "Che bello!\n[keh BEHL-loh]"),
    ("What a pity! / What a shame!\n[What sin/pity!]", "Che peccato!\n[keh pehk-KAH-toh]"),
    ("Oh my goodness!\n[My mama!]", "Mamma mia!\n[MAHM-mah MEE-ah]"),
    ("Good luck!\n[Into mouth of-the wolf!]", "In bocca al lupo!\n[een BOHK-kah ahl LOO-poh]"),
    ("Response to 'In bocca al lupo'\n[May-he die, the wolf!]", "Crepi il lupo!\n[KREH-pee eel LOO-poh]"),
    ("Makes sense / Sounds good\n[There it stays]", "Ci sta\n[chee STAH]"),
    ("Thank goodness!\n[Less bad!]", "Meno male!\n[MEH-noh MAH-leh]"),
    ("I wish! / If only!\n[Maybe! / If only!]", "Magari!\n[mah-GAH-ree]"),
    ("Come on! / Stop it!\n[Give!]", "Dai!\n[DYE]"),
    ("I don't know / Beats me!\n[(Sound of indifference)]", "Boh!\n[BOH]"),
    ("I can't wait\n[Not I see the hour]", "Non vedo l'ora\n[nohn VEH-doh LOH-rah]"),
    ("To be in a bad mood\n[To have the moon crooked]", "Avere la luna storta\n[ah-VEH-reh lah LOO-nah SKOHR-tah]"),
    ("To kill two birds with one stone\n[To take two pigeons with one fava-bean]", "Prendere due piccioni con una fava\n[PREHN-deh-reh DOO-eh pee-CHOH-nee kohn OO-nah FAH-vah]"),
    ("The sweetness of doing nothing\n[The sweet doing nothing]", "La dolce far niente\n[lah DOHL-cheh fahr NYEHN-teh]"),
    ("What a mess!\n[What casino/mess!]", "Che casino!\n[keh kah-ZEE-noh]"),
    ("Are you kidding?\n[But art-thou joking?]", "Ma stai scherzando?\n[mah stye skehr-ZAHN-doh]"),
    ("Whatever! / Forget it!\n[Leave to lose!]", "Lascia perdere!\n[LAH-shah PEHR-deh-reh]"),
    ("Exactly!\n[Exact!]", "Esatto!\n[eh-ZAHT-toh]"),
    ("Fingers crossed!\n[We cross the fingers!]", "Incrociamo le dita!\n[een-kroh-CHAH-moh leh DEE-tah]"),
    ("To cost an arm and a leg\n[To cost an eye of-the head]", "Costare un occhio della testa\n[kohs-TAH-reh oon OHK-kyoh DEHL-lah TEHS-tah]"),
    ("To hit the nail on the head\n[To hit in-the mark]", "Colpire nel segno\n[kohl-PEE-reh nehl SEHN-yoh]"),
    ("It's not a big deal\n[Not it is the end of-the world]", "Non è la fine del mondo\n[nohn eh lah FEE-neh dehl MOHN-doh]"),
    ("Out of the blue\n[At the sudden]", "All'improvviso\n[ahl-leem-prohv-VEE-zoh]"),
    ("Speak of the devil\n[Speak-thou of-the devil and sprout-they the horns]", "Parli del diavolo e spuntano le corna\n[PAHR-lee dehl DYAH-voh-loh eh SPOON-tah-noh leh KOHR-nah]"),
    ("I'm exhausted / dead tired\n[I am destroyed]", "Sono distrutto/a\n[SOH-noh dee-STROO-toh/tah]")
]

italian_set = dict(ITALIAN_PHRASES)

def play_audio(text):
    """Triggers browser native text-to-speech for the clean Italian phrase."""
    # Clean string: remove phonetic brackets and newlines before speaking
    clean_text = text.split("\n")[0].replace("'", "\\'").replace('"', '\\"')
    js_speech = f"""
    <script>
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel(); // Stop any pending speech
        var msg = new SpeechSynthesisUtterance("{clean_text}");
        msg.lang = 'it-IT';
        msg.rate = 0.9; // Slightly slower for language learners
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    st.components.v1.html(js_speech, height=0, width=0)

def app():
    st.markdown("""
    <style>
    .big-font { font-size: 18px !important; text-align: center; }
    .stButton button { height: auto !important; min-height: 70px; width: 100%; font-size: 15px; white-space: pre-wrap !important; word-wrap: break-word; padding: 0.4rem 0.5rem !important; line-height: 1.25 !important; }
    .stButton button div p { white-space: pre-wrap !important; line-height: 1.25 !important; }
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
        st.session_state.matched_history = []
        st.session_state.turns = 0
        st.session_state.team_scores = [0] * num_teams
        st.session_state.current_team = random.randint(0, num_teams - 1)
        st.session_state.audio_to_play = None
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
                
                c1_text, c1_type = st.session_state.cards[idx1]
                c2_text, c2_type = st.session_state.cards[idx2]
                eng_phrase = c1_text if c1_type == "eng" else c2_text
                ita_phrase = c2_text if c1_type == "eng" else c1_text
                
                # Queue Italian phrase audio to play
                st.session_state.audio_to_play = ita_phrase
                
                st.session_state.matched_history.append((eng_phrase, ita_phrase, team))
                st.session_state.selected = []
            else:
                st.session_state.selected = []
                st.session_state.audio_to_play = None
                st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)

    # --- Team controls ---
    if st.sidebar.button("🔀 Switch Team"):
        st.session_state.selected = []
        st.session_state.audio_to_play = None
        st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)

    # --- Play audio if match made ---
    if st.session_state.get("audio_to_play"):
        play_audio(st.session_state.audio_to_play)
        st.session_state.audio_to_play = None

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
            formatted_ita = ita.replace("\n", " ").replace("<br>", " ")
            st.markdown(
                f"**{idx}.** {formatted_eng} ↔️ **{formatted_ita}** "
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
