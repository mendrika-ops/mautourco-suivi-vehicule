$(function() {
    $( "#datefrom" ).datepicker({
       dateFormat:'yy-mm-dd',
           }).datepicker("setDate",'now');
    $( "#dateto" ).datepicker({
       dateFormat:'yy-mm-dd',
           }).datepicker("setDate",'now');   
}); 