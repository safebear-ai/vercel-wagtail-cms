const rateInputs = document.querySelectorAll('input[name="rate"]');
const thankYouMessage = document.getElementById('thankYouMessage');

rateInputs.forEach((input) => {
  input.addEventListener('change', () => {
    const selectedValue = input.value;
    console.log('Valeur sélectionnée :', selectedValue);
    
    // Afficher le message de remerciement
    thankYouMessage.style.display = 'block';
    
    // Désactiver tous les inputs pour bloquer la note
    rateInputs.forEach((input) => {
      input.disabled = true;
    });
  });
});

document.getElementById('button-addon2').addEventListener('click', function() {
    var copyText = document.getElementById('articleLink');

    // Sélectionnez et copiez le texte
    copyText.select();
    copyText.setSelectionRange(0, 99999); // Pour les appareils mobiles

    navigator.clipboard.writeText(copyText.value).then(function() {
      var successMessage = document.getElementById('copySuccessMessage');
      
      // Affichez le message avec une transition en fondu
      successMessage.style.display = 'block';
      setTimeout(function() {
        successMessage.style.opacity = 1;
      }, 10); // Petit délai pour permettre le déclenchement de la transition

      // Masquez le message après 2 secondes avec une transition en fondu
      setTimeout(function() {
        successMessage.style.opacity = 0;
        // Après la transition, masquez complètement l'élément
        setTimeout(function() {
          successMessage.style.display = 'none';
        }, 500); // Correspond à la durée de la transition opacity
      }, 2000);
    }, function(err) {
      console.error('Impossible de copier le texte : ', err);
    });
  });