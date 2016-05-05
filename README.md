# ojs harvester

Workflow semplificato per la cattura di **metadati**, pagine html (**jump off page**) e **full-text pdf** di articoli da journals [OJS](https://pkp.sfu.ca/ojs/).

La procedura inizia con un harvesting dei metadati dagli endpoint OAI-PMH. Da ogni singolo record (journal article) vengono estratte le url che lo compongono (jump off page e pdf).
Le url vengono successivamente scaricate con wget e salvate in un contenitore WARC. Vengono ulteriormente scaricate anche le pagine interstiziali di ojs per facilitare il ritrovamento dei link ai pdf durante le procedure di replay del warc.

**Nota**: i journals da archiviare devono essere preventivamente modificati con questa [patch](https://github.com/depositolegale/ojs-oai-patches) per consentire la pubblicazione nei metadati dublincore di ulteriori `<dc:identifier>` per ognuno dei full-text dell'articolo. E' una soluzione poco elegante ma necessaria per far fronte alla mancanza di formati di metadati più strutturati in ojs (esempio mpeg21-didl).



## Installazione

Requisiti: `python 2.7`, `mysql server`, `wget-lua`, `gnu parallel`.


1. installare le dipendenze python ([sickle](https://github.com/mloesch/sickle), [sqlalchemy](http://www.sqlalchemy.org/))

 		$ pip install -r requirements.txt	
 		
 	nota: viene temporaneamente installata una [versione patchata](https://github.com/atomotic/sickle/tree/patch-1) del client oaipmh Sickle, in attesa che la modifica venga riportata nel repository ufficiale.

 
2. creare un database mysql e relativo utente con privilegi

		$ mysqladmin create journals
		$ mysql -e "GRANT ALL PRIVILEGES on journals.* to journals@localhost identified by $PASSWORD"
		
3. modificare i parametri di connessione al database in `db/connection.py`

		engine = create_engine('mysql://journals:$PASSWORD@127.0.0.1:3306/journals?charset=utf8')
		
4. creare le tabelle del database

		$ python -c "import db.model"
		
		
		
## Utilizzo		

1. **configurare i journals da harvestare**  
popolare la tabella `sites` con i dati dei journals (id del repository, url oaipmh, email di contatto, metadata format, set)

	esempio:

		mysql journals  
		mysql> INSERT INTO sites (name, url, contact, format, sets) VALUES ("unibo.series", "http://series.unibo.it/oai", "email@", "oai_dc", "all");
			   	
2. **catturare i metadati della rivista**

		python harvest.py {site.id}
		
	esempio:
		
		$ python harvest.py unibo.series
		
	per lanciare catture multiple in parallelo (es. 10):
	
		$ mysql journals -N -s -e "SELECT name FROM sites" | parallel -j10 python harvest.py {}	
		
		
3. **generare il seed file** (viene salvato in `./data/seeds`)

		python seed.py {site.id}

	esempio

		$ python seed.py unibo.series
		
	per generarli in parallelo:
	
		$ mysql journals -N -s -e "SELECT name FROM sites" | parallel -j10 python seed.py {}	
		
4. **archiviare le url**

	per la cattura delle pagine web e i relativi full-text pdf è necessario installare [wget-lua](http://www.archiveteam.org/index.php?title=Wget_with_Lua_hooks) (istruzioni: [linux](https://raw.githubusercontent.com/ArchiveTeam/gamefront-grab/master/get-wget-lua.sh), [osx](https://gist.github.com/atomotic/81f07f880e0d09915aea8d33d81d70bb)). lo script `ojs.lua` permette a runtime di aggiungere alle url definite nel seedfile anche le pagine interstiziali di ojs (dove un viewer web visualizza il pdf). Queste pagine sono necessarie per una corretta visualizzazione durante il replay.
	
		archive.sh {seedfile}

	esempio

		$ archive.sh data/seeds/20160504-unibo.series.seeds
		
	in `./data/warc` viene salvato un file [WARC](https://en.wikipedia.org/wiki/Web_ARChive) contentente le risorse web archiviate.
	
	Il file WARC è pronto per essere depositato (ingest) nel sistema di conservazione, dove verrà indicizzato e reso accessibile da un'applicazione di replay di archivi web (openwayback o pywb)


 
	


















			