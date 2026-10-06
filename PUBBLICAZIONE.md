# Pubblicazione gratuita su GitHub Pages

L'app pronta Contatto.html è autonoma. Il workflow .github/workflows/pages.yml pubblica soltanto questo file come index.html; non include Word originali, script o file di lavoro.

Prerequisito dell'account: in Matteoago3113/contatto_clienti, aprire Settings → Pages → Build and deployment → Source e selezionare GitHub Actions. GitHub Pages deve essere disponibile per il piano e la visibilità del repository; su GitHub Free è disponibile per repository pubblici. Non cambiare la visibilità di un repository privato senza una decisione esplicita del proprietario.

Dopo il caricamento del progetto sul ramo main, il workflow pubblica l'app. Un collegamento è da considerare attivo soltanto dopo il completamento del workflow e la verifica HTTP della pagina.

L'app pubblicata rende accessibili i modelli dei messaggi. I dati compilati dai visitatori restano nel browser e non vengono inviati al server. Questa versione non invia email o WhatsApp e non accede al database.
