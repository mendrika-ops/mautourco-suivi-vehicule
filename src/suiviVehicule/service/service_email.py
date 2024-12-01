from django.core.mail import send_mail
from django.utils.timezone import now
from suiviVehicule.models import RapportAuto, LogRapportAuto, TypeRapport
from django.contrib.auth.models import User, Group
from django.conf import settings
class EmailService:
    def get_destinataire(self, group_id):
        group = Group.objects.get(id=group_id)    
        users = group.user_set.all() 
        return users
    
    def send_mail_weekly(self):
        group = Group.objects.get(id=2)  #Departement RH
        type_rapport = TypeRapport.objects.get(id=2) #hebdomadaire
        users = self.get_destinataire(group.id)
        sujet = f"Automatic Report : weekly, local HR representative"
        message = (
            "Dear Team,\n\n"
            "Here is the weekly report from the local HR representative. This report summarizes key resource updates for the past week, "
            "highlighting the top-performing drivers and their achievements.\n\n"
            "Key points include:\n"
            "- Overview of resource allocation and utilization.\n"
            "- Recognition of top drivers based on performance metrics.\n"
            "- Insights into areas for improvement and upcoming priorities.\n\n"
            "Please review the report and let us know if you have any questions or need further details.\n\n"
            "Best regards,\n"
            "Vehicle fleet"
        )

        return self.sender_mail(type_rapport, group, users, sujet, message)
        

    def send_mail_monthly(self):
        group = Group.objects.get(id=2) #Direction de l'évaluation, de la prospective et de la performance
        type_rapport = TypeRapport.objects.get(id=3) #mensuelle
        users = self.get_destinataire(group.id)
        sujet = f"Monthly Report - Statistics Department"
        message = """
            Dear Team,

            The Monthly Report from the Statistics Department is now available. This report provides an overview of key performance indicators, comparative analysis, and actionable insights to guide our decisions moving forward.

            Key highlights in this report include:
            - A comprehensive analysis of the performance metrics.
            - Identification of trends and opportunities for growth.
            - Recommendations for addressing the challenges identified.

            Please review the document at your earliest convenience and share any questions or feedback during our upcoming team meeting.

            Thank you for your attention and continued dedication to our objectives.

            Best regards,
            Vehicle fleet
            """

        return self.sender_mail(type_rapport, group, users, sujet, message)
        print("test")

    def sender_mail(self, type_rapport, group, users, sujet, message):
        try:
            destinataires = [user.email for user in users if user.email]

            send_mail(sujet, message, settings.DEFAULT_FROM_EMAIL, destinataires)

            rapport = RapportAuto.objects.create(
                title=sujet,
                description=message,
                created_at=now(),
                is_active=True,
                sent_to=group,
                type_rapport=type_rapport
            )

            self.create_log(users, rapport, "Email envoyé avec succès", "200")
    
        except Exception as e:
            self.create_log(users, rapport, str(e), "400")
            return str(e)
        return "Ok"
           
    def create_log(self, users, rapport, result, status):
        for user in users:
            if not LogRapportAuto.objects.filter(
                recipient=user.email,
                rapport_auto=rapport,
                status=status
            ).exists():
                LogRapportAuto.objects.create(
                    recipient=user.email,
                    result=result,
                    status=status,
                    created_at=now(),
                    rapport_auto=rapport,
                    user=user
                )