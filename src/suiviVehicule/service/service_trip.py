
from suiviVehicule.models import *
from datetime import datetime
from suiviVehicule.state import State
import random
class TripService:
    def __init__(self) -> None:
        pass

    def get_reason_list(self):
        return ReasonCancel.objects.filter(is_active=True).order_by('order')
    
    def get_subreason_list(self):
        return SubReasonCancel.objects.filter(is_active=True).order_by('order')
    
    def get_reason_by_id(self, id_reason):
        return ReasonCancelRecord.objects.filter(reason=id_reason)
    
    def get_subreason_recorded_current(self, id_trip):
        record = Recordcomment.objects.filter(id_trip=id_trip, etat=7).first()
        return SubReasonCancelRecordV1.objects.filter(record_comment_sub_id=record.id, state = State.CREATED.value).all() if record is not None else SubReasonCancelRecordV1.objects.none()

    def save_subreason_record(self, record, id_sub_reasons):
        try:
            for id_subreason in id_sub_reasons:
                self.save_subreason_one_record(record, id_subreason)
            
        except Exception as a:
            raise a

    def save_subreason_one_record(self, record, id_subreason):
        if not SubReasonCancelRecord.objects.filter(record_comment_sub_id = record.id, sub_reason_id = id_subreason).exists():
            subreason = SubReasonCancel.objects.filter(id = id_subreason).first() 
            subreason_record = SubReasonCancelRecord()
            setattr(subreason_record, 'record_comment_sub', record)
            setattr(subreason_record, 'sub_reason', subreason)
            setattr(subreason_record, 'state', State.CREATED.value)
            print(subreason_record)
            subreason_record.save()
        else:
            subreason = SubReasonCancelRecord.objects.filter(record_comment_sub_id = record.id, sub_reason_id = id_subreason).first()
            setattr(subreason, 'state', State.CREATED.value)
            subreason.save() 

    def save_reason_record(self, record, id_reason):
        try:
            if not ReasonCancelRecord.objects.filter(record_comment_id = record.id, reason_id = id_reason).exists():
                reason = ReasonCancel.objects.filter(id = id_reason).first() 
                reason_record = ReasonCancelRecord()
                setattr(reason_record, 'record_comment', record)
                setattr(reason_record, 'reason', reason)
                reason_record.save()
        except Exception as a:
            raise a

    def save_record_comment(self,id_trip, comment, date, status):
        if self.checkexist(id_trip):
            raise Exception("Error! Already canceled")
        else:
            data = Trajetcoordonnee.objects.filter(id_trip=id_trip)
            row = data[0]
            record = Recordcomment()
            record.comment = comment
            record.id_trip = id_trip
            record.datetime = date
            record.vehicleno = row.vehicleno
            record.driver_oname = row.driver_oname
            record.FromPlace = row.FromPlace
            record.ToPlace = row.ToPlace
            record.trip_start_date = row.trip_start_date
            record.pick_up_time = row.pick_up_time
            record.driver_mobile_number = row.driver_mobile_number
            record.etat = status

            record.save()

        return Recordcomment.objects.filter(id_trip=id_trip,etat=status).first()
    
    def checkexist(self, id_trip):
        return Recordcomment.objects.filter(id_trip=id_trip,etat=State.WAITING.value).exists()
    
    def sub_record_json_to_object(self, sub_reasons):
        subs = []
        for i in range(len(sub_reasons)):
            reason = SubReasonCancelRecord()
            setattr(reason, 'id', sub_reasons[i]["id"])
            subs.append(reason)
        return subs
    
    def change_state_reason_record(self, id_trip, reason_id,sub_reason_rec_ids, state):
        record = Recordcomment.objects.filter(id_trip=id_trip, etat=State.WAITING.value).first()
        for sub_reason_rec_id in sub_reason_rec_ids:
            sub_reason_rec = SubReasonCancelRecord.objects.filter(id=sub_reason_rec_id.id, record_comment_sub=record.id, state=State.CREATED.value).first()   
            setattr(sub_reason_rec, 'state', state)
            sub_reason_rec.save()        
        
    def update_record_random(self):
        subreasons = SubReasonCancel.objects.filter()

        elements = [(index, subreason.sub_reason_name) for index, subreason in enumerate(subreasons)]
        quotas = [subreason.order for subreason in subreasons]

        k = random.choice([2,1,4])

        records = Recordcomment.objects.filter(etat=0, catno=10)
        for record in records:
            random_choices = random.sample(random.choices(elements, weights=quotas, k=len(elements)), k=k)
            comment = ""
            for rand in set(random_choices):
                print("indroo "+ record.comment+ " ::: "+ str(rand[1]) + " : "+ subreasons[rand[0]].sub_reason_name)
                subreason_id = subreasons[rand[0]].id
                reason_id = subreasons[rand[0]].reason_id
                #self.save_reason_record(record, reason_id)
                #self.save_subreason_one_record(record, subreason_id)
                comment+= subreasons[rand[0]].sub_reason_name + ", "
            setattr(record, "comment", comment)
            #record.save()
            print("Élément sélectionné : ", comment)

    def get_record_comment(self, id_trip):
        record = Recordcomment.objects.filter(id_trip=id_trip).first()
        return record
    
    def record_change_state(self, id_trip, status):
        rec = self.get_record_comment(id_trip)  
        if status == 1:
            #change status to canceled
            rec.etat = State.CANCELED_TRIP.value
            rec.save()
        elif status == 0:
            rec.delete()
            pass
        
    
            


        

