var graph = JSON.parse($('#myChart').attr('data'));

var xValues = graph['label'];
var yValues = graph['data'];
var click = true;
var barColors = graph['couleur'];

var canvasP = document.getElementById("myChart");

let myChart = new Chart("myChart", {
    type: "pie",
    data: {
        labels: xValues,
        datasets: [{
            backgroundColor: barColors,
            data: yValues
        }]
    },
    options: {
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
                let datasets = ctx.chart.data.datasets;
                if (datasets.indexOf(ctx.dataset) === datasets.length - 1) {
                  return value;
                } else {
                  return percentage;
                }
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
   location.href = "/dashboard?driver_oname=&FromPlace=&driver_mobile_number=&ToPlace=&vehicleno=&status="+label+"&id_trip=&trip_no=";
}
