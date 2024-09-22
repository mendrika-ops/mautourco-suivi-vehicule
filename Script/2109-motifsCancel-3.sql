select * from suivivehicule_recordcomment sr where etat = 2;

select * from suivivehicule_statusposdetail ss ;

select * from suivivehicule_statusparameter ss ;

select * from suivivehicle_laststatus ; 

INSERT INTO `suivivehicule_reasoncancel` (`reason_name`, `reason_description`, `is_active`, `created_at`)
VALUES 
('Problème Véhicule', 'Annulation due à un problème mécanique ou accident.', 1, NOW()),
('Problème Chauffeur', 'Annulation due à un problème avec le chauffeur.', 1, NOW()),
('Conditions Météo', 'Annulation due à des conditions météorologiques dangereuses.', 1, NOW()),
('Problème Client', 'Annulation causée par un problème du côté du client.', 1, NOW()),
('Annulation Externe', 'Annulation causée par une tierce partie ou une situation imprévue.', 1, NOW());

INSERT INTO `suivivehicule_subreasoncancel` (`sub_reason_name`, `sub_reason_description`, `is_active`, `created_at`, `reason_id`)
VALUES 
('Moteur défaillant', 'Le moteur du véhicule ne fonctionne pas correctement.', 1, NOW(), 1),
('Panne de batterie', 'Le véhicule est en panne à cause d\'une batterie défectueuse.', 1, NOW(), 1),
('Accident', 'Le véhicule a été impliqué dans un accident.', 1, NOW(), 1),
('Pneus crevés', 'Un ou plusieurs pneus sont crevés.', 1, NOW(), 1),
('Problème de freins', 'Les freins du véhicule ne fonctionnent pas.', 1, NOW(), 1),
('Problème de transmission', 'La transmission du véhicule ne répond pas.', 1, NOW(), 1),
('Maladie', 'Le chauffeur est malade et incapable de conduire.', 1, NOW(), 2),
('Absence non prévue', 'Le chauffeur n\'est pas disponible au moment du départ.', 1, NOW(), 2),
('Problème de permis', 'Le chauffeur n\'a pas de permis valide.', 1, NOW(), 2),
('Comportement inapproprié', 'Le chauffeur a eu un comportement inapproprié.', 1, NOW(), 2),
('Retard du chauffeur', 'Le chauffeur est en retard.', 1, NOW(), 2),
('Chauffeur non assigné', 'Aucun chauffeur n\'a été assigné à ce trajet.', 1, NOW(), 2),
('Pluie abondante', 'Conditions météorologiques dangereuses dues à la pluie.', 1, NOW(), 3),
('Neige/Glace', 'Annulation due à des conditions enneigées ou glacées.', 1, NOW(), 3),
('Vent violent', 'Conditions de vent dangereux.', 1, NOW(), 3),
('Tempête', 'Une tempête violente empêche le trajet.', 1, NOW(), 3),
('Brouillard dense', 'Le trajet est dangereux à cause du brouillard.', 1, NOW(), 3),
('Inondation', 'Le trajet est impraticable en raison d\'inondations.', 1, NOW(), 3),
('Annulation de dernière minute', 'Le client a annulé juste avant le départ.', 1, NOW(), 4),
('Absence au point de rendez-vous', 'Le client n\'est pas arrivé au point de rendez-vous.', 1, NOW(), 4),
('Erreur de réservation', 'Le client a mal réservé son trajet.', 1, NOW(), 4),
('Changement de destination', 'Le client a modifié la destination.', 1, NOW(), 4),
('Problème de paiement', 'Le client n\'a pas payé pour le trajet.', 1, NOW(), 4),
('Retard du client', 'Le client est en retard.', 1, NOW(), 4),
('Grève', 'Une grève empêche le trajet.', 1, NOW(), 5),
('Interruption du service', 'Le service est interrompu à cause de causes externes.', 1, NOW(), 5),
('Fermeture de route', 'Les routes sont fermées à cause de travaux ou d\'accidents.', 1, NOW(), 5),
('Incident de sécurité', 'Un incident de sécurité a interrompu le trajet.', 1, NOW(), 5),
('Pandémie', 'La pandémie a empêché le trajet.', 1, NOW(), 5),
('Catastrophe naturelle', 'Une catastrophe naturelle a empêché le trajet.', 1, NOW(), 5);
