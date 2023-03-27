var graph = JSON.parse($('#myChart').attr('data'));

var xValues = graph['label'];
var labels = []
var yValues = graph['data'];
total = yValues.reduce((accumulator, currentValue) => accumulator + currentValue);
for(var i =0 ; i< yValues.length; i++){
    labels[i] = Math.round((yValues[i] / total) * 100) + '%'+' '+xValues[i];
}
var click = true;
var barColors = graph['couleur'];

var canvasP = document.getElementById("myChart");

let myChart = new Chart("myChart", {
    type: "pie",
    data: {
        labels: labels,
        datasets: [{
            backgroundColor: barColors,
            data: yValues
        }]
    },
    options: {
        aspectRatio: 3,
        onHover: (evt, activeEls) => {
            console.log("event ", evt);
            activeEls.length > 0 ? evt.target.style.cursor = 'pointer' : evt.target.style.cursor = 'default';
        },
        title: {
            display: true,
            text: "Dashboard",
            fontSize: 40,
            fontColor: '#105378',
        },
        legend: {
            position: 'left',
        },
        plugins: {
            datalabels: {
                formatter: (value, ctx) => {
                    let sum = ctx.dataset._meta[0].total;
                    let percentage = (value * 100 / sum).toFixed(1) + "%";
                    return value;
                },
                display: true,
                color: 'black',
                style: {
                   fontWeight: 'bold'
                }
            }
        }
    },
});

function clickIcon(){
    if(click){
        $('.carrosell').find('i').css('transform','rotate(-90deg)');
        click = false;
    }else{
        $('.carrosell').find('i').css('transform','rotate(90deg)');
        click = true;
    }
    
}

canvasP.onclick = function(e) {
   var slice = myChart.getElementAtEvent(e);
   if (!slice.length) return; 
   console.log(slice[0]._model.value)
   let label = slice[0]._model.label;
   location.href = "/dashboard?driver_oname=&FromPlace=&driver_mobile_number=&ToPlace=&vehicleno=&status="+label.split('%')[1]+"&id_trip=&trip_no=";
}
