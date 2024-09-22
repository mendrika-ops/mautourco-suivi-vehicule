document.addEventListener('DOMContentLoaded', function() {
    const reasonSelect = document.getElementById('reason');
    const subReasonsDiv = document.getElementById('sub-reasons');
    const selectedReasonsContainer = document.getElementById('selected-reasons-container');

    reasonSelect.addEventListener('change', function() {
        const selectedReasonId = this.value;
        subReasonsDiv.innerHTML = '';

        if (selectedReasonId) {
            const filteredSubReasons = subReasons.filter(subReason => subReason.reason == selectedReasonId);
            if (filteredSubReasons.length > 0) {
                filteredSubReasons.forEach(subReason => {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = 'sub_reasons';
                    checkbox.value = subReason.id;

                    const label = document.createElement('label');
                    label.textContent = subReason.sub_reason_name;

                    subReasonsDiv.appendChild(checkbox);
                    subReasonsDiv.appendChild(label);
                    subReasonsDiv.appendChild(document.createElement('br'));
                });
            } else {
                subReasonsDiv.innerHTML = '<p>Aucun sous-motif disponible pour ce motif.</p>';
            }
        }
    });

    // Grouper par raison
function groupByReason(data) {
    return data.reduce((acc, item) => {
        // Assurez-vous que reason_id existe dans chaque item
        if (!acc[item.reason_name]) {
            acc[item.reason_name] = {
                reason_id: item.reason_id || 'ID non défini', // Ajoutez un fallback pour tester
                sub_reasons: [] // Tableau des sous-motifs associés à cette raison
            };
        }

        // Ajouter chaque sous-motif à la raison correspondante
        acc[item.reason_name].sub_reasons.push(item);
        return acc;
    }, {});
}

function updateCurrentReasons() {
    fetch(`/trip/cancel/get_current_reasons/` + id_trip)
        .then(response => response.json())
        .then(data => {
            selectedReasonsContainer.innerHTML = ''; // Vider le conteneur avant de recharger

            if (data.length > 0) {
                // Grouper les raisons par reason_name
                const groupedReasons = groupByReason(data);

                // Pour chaque raison
                Object.keys(groupedReasons).forEach(reasonName => {
                    const reasonData = groupedReasons[reasonName];
                    const reasonCard = document.createElement('div');
                    reasonCard.classList.add('reason-card');

                    // Titre du motif
                    const reasonHeader = document.createElement('h4');
                    reasonHeader.textContent = reasonName;

                    // Icône de suppression de la raison
                    const deleteIcon = document.createElement('span');
                    deleteIcon.innerHTML = '❌';
                    deleteIcon.style.cursor = 'pointer';
                    deleteIcon.addEventListener('click', () => {
                        console.log("Supprimer reason_id:", reasonData.reason_id);
                        removeReason(reasonData.reason_id, reasonData.sub_reasons); // Utiliser le reason_id pour suppression
                    });

                    reasonHeader.appendChild(deleteIcon);
                    reasonCard.appendChild(reasonHeader);

                    // Ajouter les sous-motifs associés
                    reasonData.sub_reasons.forEach(subReason => {
                        const subReasonText = document.createElement('p');
                        subReasonText.textContent = subReason.sub_reason_name;

                        // Icône de suppression pour chaque sous-motif
                        const subReasonDeleteIcon = document.createElement('span');
                        subReasonDeleteIcon.innerHTML = '❌';
                        subReasonDeleteIcon.style.cursor = 'pointer';
                        subReasonDeleteIcon.addEventListener('click', () => {
                            console.log("Supprimer sub_reason_id:", subReason.id);
                            let subs = [];
                            subs.push(subReason)
                            removeReason(reasonData.reason_id, subs);
                        });

                        subReasonText.appendChild(subReasonDeleteIcon);
                        reasonCard.appendChild(subReasonText);
                    });

                    selectedReasonsContainer.appendChild(reasonCard);
                });
            } else {
                selectedReasonsContainer.innerHTML = '<p>Aucune raison ajoutée.</p>';
            }
        })
        .catch(error => console.error('Error fetching current reasons:', error));
}


     // Validation du formulaire avant soumission
     const cancelTripForm = document.getElementById('cancel-trip-form');
    cancelTripForm.addEventListener('submit', function(event) {
        const reasonSelected = reasonSelect.value;
        const reasonText = reasonSelect.options[reasonSelect.selectedIndex].text;
        const subReasonsChecked = document.querySelectorAll('input[name="sub_reasons"]:checked');
        
        if (!reasonSelected) {
            alert('Veuillez sélectionner un motif.');
            event.preventDefault();
        } else if (subReasonsChecked.length === 0) {
            alert('Veuillez sélectionner au moins un sous-motif.');
            event.preventDefault();
        } else {
            const subReasonIdsArray = Array.from(subReasonsChecked).map(checkbox => checkbox.value);

            persistSelection(reasonSelected, subReasonIdsArray);
            event.preventDefault();
        }
    });

    // Fonction pour persister la sélection et mettre à jour l'affichage
    function persistSelection(reasonId, subReasonIds) {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch('/trip/cancel/save/' + id_trip, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                reason_id: reasonId,
                sub_reason_ids: subReasonIds
            })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  console.log('Data persisted successfully');
                  updateCurrentReasons(); // Mettre à jour la liste des raisons après persistance
              } else {
                  console.error('Error persisting data');
              }
          }).catch(error => console.error('Error:', error));
    }

    // Fonction pour supprimer un motif complet
    function removeReason(reasonId, sub_reasons) {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log("reason id ",sub_reasons)
        fetch(`/trip/cancel/remove_reason/` + id_trip, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 
                reason_id: reasonId,
                sub_reason_ids: sub_reasons
            })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  console.log('Reason removed successfully');
                  updateCurrentReasons();
              } else {
                  console.error('Error removing reason');
              }
          }).catch(error => console.error('Error:', error));
    }

    updateCurrentReasons();
});