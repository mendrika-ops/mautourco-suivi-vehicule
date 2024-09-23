import xlwt
from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from suiviVehicule.models import Recordexport
class Export:

    def __init__(self) -> None:
        pass

    def export_record(self, datefrom, dateto):
        dateinfrom = datetime. strptime(datefrom, '%Y-%m-%d')
        dateinto = datetime. strptime(dateto, '%Y-%m-%d')
        filename = "log_data_"+ datefrom +"_"+dateto+".xls" 
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename='+filename

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Driver name', 'Driveer Mob No','Vehicule No', 'Trip ID' ,  'Pickup Place', 'Destination' ,'Current postion', 'Pick up time', 'Date' , 'Actual Time', 'Difference' , 'Comments', 'Status']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = Recordexport.objects.filter(daterecord__range = [dateinfrom,dateinto]).values_list( 'driver_oname', 'driver_mobile_number','vehicleno', 'id_trip', 'FromPlace','ToPlace', 'current' , 'pick_up_time', 'daterecord','actualtime', 'difftimepickup', 'comment', 'status').order_by('daterecord','actualtime')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
        
