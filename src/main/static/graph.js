var graph = JSON.parse($('#myChart').attr('data'));

var xValues = graph['label'];
var yValues = graph['data'];
var click = true;
var barColors = graph['couleur'];

new Chart("myChart", {
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
