async function fetchCard() {
            const bookId = document.getElementById("bookId").value.trim();
            if (!bookId) return;

            document.getElementById("loading").style.display = "block";
            document.getElementById("card").style.display = "none";
            document.getElementById("error").style.display = "none";

            try {
                const response = await fetch(`/card/${bookId}`);
                
                if (!response.ok) {
                    throw new Error("Not found");
                }

                const data = await response.json();

                document.getElementById("title").textContent = data.title || "Sans titre";

                document.getElementById("authors").textContent = data.info?.authors || "Inconnu";
                document.getElementById("bookshelves").textContent = data.info?.bookshelves || "Non classé";

                //lexical diversity
                document.getElementById("tok").textContent = data.lexdiv?.tok || 0;
                document.getElementById("typ").textContent = data.lexdiv?.typ || 0;
                document.getElementById("ttr").textContent = data.lexdiv?.ttr ? data.lexdiv.ttr.toFixed(4) : "0.0000";
                document.getElementById("hap").textContent = data.lexdiv?.hap || 0;

                //personnages
                const charsDiv = document.getElementById("characters");
                charsDiv.innerHTML = data.entities?.characters?.length 
                    ? data.entities.characters.map(c => `<span class="tag">${c}</span>`).join("")
                    : "<em>Aucun personnage trouvé</em>";

                //lieux
                const locsDiv = document.getElementById("locations");
                locsDiv.innerHTML = data.entities?.locations?.length 
                    ? data.entities.locations.map(l => `<span class="tag">${l}</span>`).join("")
                    : "<em>Aucun lieu trouvé</em>";

                // livres similaires    
                const similarDiv = document.getElementById("similar");
                if (data.similar && data.similar.length > 0) {
                similarDiv.innerHTML = data.similar.map(title => `<span class="tag">${title}</span>`).join("");
                } else {
                similarDiv.innerHTML = "<em>Aucun livre similaire dans la collection</em>";
                }
                

                //résumé
                document.getElementById("summary").textContent = data.summary || "Pas de résumé disponible.";

                //affichage
                document.getElementById("loading").style.display = "none";
                document.getElementById("card").style.display = "block";

            //gestion des erreurs    
            } catch (err) {
                document.getElementById("loading").style.display = "none";
                document.getElementById("error").style.display = "block";
            }
        }