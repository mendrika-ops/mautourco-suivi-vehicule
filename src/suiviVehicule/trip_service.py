
from suiviVehicule.models import *
from datetime import datetime
from suiviVehicule.state import State
class TripService:
    def __init__(self) -> None:
        pass

    def get_reason_list(self):
        return ReasonCancel.objects.filter(is_active=True)
    
    def get_subreason_list(self):
        return SubReasonCancel.objects.filter(is_active=True) 
    
    def get_reason_by_id(self, id_reason):
        return ReasonCancelRecord.objects.filter(reason=id_reason)
    
    def get_subreason_recorded_current(self, id_trip):
        record = Recordcomment.objects.filter(id_trip=id_trip, etat=0).first()
        return SubReasonCancelRecordV1.objects.filter(record_comment_sub_id=record.id, state = State.CREATED.value).all() if record is not None else SubReasonCancelRecordV1.objects.none()

    def save_subreason_record(self, record, id_sub_reasons):
        try:
            for id_subreason in id_sub_reasons:
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
            
        except Exception as a:
            raise a
        
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

    def save_record_comment(self,id_trip, comment):
        if self.checkexist(id_trip):
            pass
        else:
            data = Trajetcoordonnee.objects.filter(id_trip=id_trip)
            row = data[0]
            record = Recordcomment()
            record.comment = comment
            record.id_trip = id_trip
            record.datetime = datetime.now() 
            record.vehicleno = row.vehicleno
            record.driver_oname = row.driver_oname
            record.FromPlace = row.FromPlace
            record.ToPlace = row.ToPlace
            record.trip_start_date = row.trip_start_date
            record.pick_up_time = row.pick_up_time
            record.driver_mobile_number = row.driver_mobile_number
            record.etat = State.CANCELED.value

            record.save()

        return Recordcomment.objects.filter(id_trip=id_trip,etat=State.CANCELED.value).first()
    
    def checkexist(self, id_trip):
        return Recordcomment.objects.filter(id_trip=id_trip,etat=State.CANCELED.value).exists()
    
    def sub_record_json_to_object(self, sub_reasons):
        subs = []
        for i in range(len(sub_reasons)):
            reason = SubReasonCancelRecord()
            setattr(reason, 'id', sub_reasons[i]["id"])
            subs.append(reason)
        return subs
    
    def change_state_reason_record(self, id_trip, reason_id,sub_reason_rec_ids, state):
        record = Recordcomment.objects.filter(id_trip=id_trip, etat=State.CANCELED.value).first()
        for sub_reason_rec_id in sub_reason_rec_ids:
            sub_reason_rec = SubReasonCancelRecord.objects.filter(id=sub_reason_rec_id.id, record_comment_sub=record.id, state=State.CREATED.value).first()   
            setattr(sub_reason_rec, 'state', state)
            sub_reason_rec.save()
    


        

